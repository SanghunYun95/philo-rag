import json
import asyncio
from fastapi import APIRouter, Request
from pydantic import BaseModel
from sse_starlette.sse import EventSourceResponse

from app.services.llm import get_english_translation, get_response_stream
from app.services.embedding import embedding_service
from app.services.database import supabase_client

router = APIRouter()

class ChatRequest(BaseModel):
    query: str

async def generate_chat_events(request: Request, query: str):
    """
    Generator function that streams SSE events.
    It yields 'metadata' first, then chunks of 'content'.
    """
    # 1. Translate Korean query to English
    try:
        english_query = get_english_translation(query)
    except Exception as e:
        yield {"event": "error", "data": "오늘은 철학자도 사색의 시간이 필요하답니다. 내일 다시 지혜를 나누러 올게요."}
        return
    
    # 2. Generate vector representation
    query_vector = embedding_service.generate_embedding(english_query)
    
    # 3. Perform hybrid search in Supabase
    # We use the RPC match_documents function defined in schema.sql
    try:
        response = supabase_client.rpc(
            'match_documents', 
            {'query_embedding': query_vector, 'match_count': 3}
        ).execute()
        documents = response.data
    except Exception as e:
        yield {"event": "error", "data": f"Database search failed: {str(e)}"}
        return
        
    if not documents:
        yield {"event": "content", "data": "관련 철학적 내용을 찾을 수 없습니다."}
        return

    # 4. Extract contexts and format metadata
    contexts = []
    philosophers_meta = []
    
    for doc in documents:
        contexts.append(doc['content'])
        meta = doc['metadata']
        # Group metadata to send to the frontend
        if meta not in philosophers_meta:
            philosophers_meta.append(meta)

    # 5. Emit Event 1: metadata (Structured JSON)
    metadata_event = {
        "philosophers": philosophers_meta
    }
    yield {"event": "metadata", "data": json.dumps(metadata_event, ensure_ascii=False)}

    # Add a small delay for frontend to process metadata before sending content
    await asyncio.sleep(0.1)

    # 6. Emit Event 2: content (Text chunk streaming via LLM)
    combined_context = "\n\n".join(contexts)
    
    try:
        llm_stream = get_response_stream(context=combined_context, query=english_query)
        
        for chunk in llm_stream:
            # If client disconnects, stop generating
            if await request.is_disconnected():
                break
                
            # Clean up chunk to avoid SSE formatting issues with newlines
            chunk_clean = chunk.replace("\n", "\\n")
            yield {"event": "content", "data": chunk_clean}
    except Exception as e:
        yield {"event": "error", "data": "오늘은 철학자도 사색의 시간이 필요하답니다. 내일 다시 지혜를 나누러 올게요."}
        return

@router.post("")
async def chat_endpoint(request: Request, chat_request: ChatRequest):
    """
    Endpoint for accepting chat queries and returning a text/event-stream response.
    """
    return EventSourceResponse(generate_chat_events(request, chat_request.query))
