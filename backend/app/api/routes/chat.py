import json
import asyncio
import logging
from typing import List, Dict, Optional
from fastapi import APIRouter, Request, Depends
from pydantic import BaseModel, Field
from sse_starlette.sse import EventSourceResponse

from app.services.llm import get_english_translation, get_response_stream_async
from app.services.embedding import embedding_service
from app.services.database import get_client
from app.core.rate_limit import limiter

router = APIRouter()
logger = logging.getLogger(__name__)

class HistoryMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    query: str
    history: List[HistoryMessage] = Field(default_factory=list)

def _search_documents(query_vector):
    return get_client().rpc(
        'match_documents', 
        {'query_embedding': query_vector, 'match_count': 3}
    ).execute()

async def generate_chat_events(request: Request, query: str, history: List[HistoryMessage]):
    """
    Generator function that streams SSE events.
    It yields 'metadata' first, then chunks of 'content'.
    """
    # 1. Translate Korean query to English // Note: We don't translate history here to save costs and reduce latency
    try:
        english_query = await asyncio.to_thread(get_english_translation, query)
    except Exception:
        logger.exception("Failed to translate query")
        yield {"event": "error", "data": "오늘은 철학자도 사색의 시간이 필요하답니다. 내일 다시 지혜를 나누러 올게요."}
        return
    
    # 2. Generate vector representation
    try:
        query_vector = await asyncio.to_thread(embedding_service.generate_embedding, english_query)
    except Exception:
        logger.exception("Failed to generate query embedding")
        yield {"event": "error", "data": "오늘은 철학자도 사색의 시간이 필요하답니다. 내일 다시 지혜를 나누러 올게요."}
        return
    
    # 3. Perform hybrid search in Supabase
    # We use the RPC match_documents function defined in schema.sql
    try:
        response = await asyncio.to_thread(_search_documents, query_vector)
        documents = response.data
    except Exception:
        logger.exception("Database search failed")
        yield {"event": "error", "data": "검색 중 오류가 발생했습니다. 잠시 후 다시 시도해 주세요."}
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
    
    MAX_HISTORY_MESSAGES = 20
    MAX_HISTORY_CHARS = 1000
    history_tail = (history or [])[-MAX_HISTORY_MESSAGES:]
    formatted_parts: List[str] = []

    for msg in history_tail:
        role = str(msg.role or "").lower()
        if role == "user":
            role_name = "User"
        elif role in ("ai", "agent", "philorag"):
            role_name = "Agent (PhiloRAG)"
        else:
            continue
        content = (msg.content or "").strip()
        if not content:
            continue
        formatted_parts.append(f"{role_name}: {content[:MAX_HISTORY_CHARS]}")

    formatted_history = "\n\n".join(formatted_parts)
            
    try:
        async for chunk in get_response_stream_async(context=combined_context, query=english_query, history=formatted_history):
            # If client disconnects, stop generating
            if await request.is_disconnected():
                break
                
            # Clean up chunk to avoid SSE formatting issues with newlines
            chunk_clean = chunk.replace("\n", "\\n")
            yield {"event": "content", "data": chunk_clean}
    except Exception:
        logger.exception("Failed while streaming LLM response")
        yield {"event": "error", "data": "오늘은 철학자도 사색의 시간이 필요하답니다. 내일 다시 지혜를 나누러 올게요."}
        return

@router.post("")
@limiter.limit("5/minute")
async def chat_endpoint(request: Request, chat_request: ChatRequest):
    """
    Endpoint for accepting chat queries and returning a text/event-stream response.
    """
    return EventSourceResponse(generate_chat_events(request, chat_request.query, chat_request.history))
