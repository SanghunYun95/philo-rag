import json
import asyncio
import logging
import time
from typing import List, Dict, Optional
from fastapi import APIRouter, Request, Depends
from pydantic import BaseModel, Field
from sse_starlette.sse import EventSourceResponse

from app.services.database import get_client
from app.core.rate_limit import limiter

router = APIRouter()
logger = logging.getLogger(__name__)

DEFAULT_CHAT_TITLE = "새로운 대화"
CHAT_TIMEOUT = 30.0

# Concurrency limit for database RPC calls to prevent thread pool exhaustion
_db_rpc_semaphore = asyncio.Semaphore(16)

class HistoryMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    query: str
    history: List[HistoryMessage] = Field(default_factory=list)

class TitleRequest(BaseModel):
    query: str = Field(..., max_length=1024)

def _search_documents(query_vector):
    return get_client().rpc(
        'match_documents', 
        {'query_embedding': query_vector, 'match_count': 3}
    ).execute()

from fastapi import APIRouter, Request, Depends, BackgroundTasks

async def generate_chat_events(request: Request, query: str, history: List[HistoryMessage], background_tasks: BackgroundTasks = None):
    """
    Generator function that streams SSE events using LangGraph.
    """
    from app.services.graph import create_graph
    
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
    
    t0 = time.perf_counter()
    graph = create_graph()
    
    metadata_sent = False
    full_answer = ""
    chunk_count = 0
    final_state = {}
    client_disconnected = False
    
    try:
        async for event in graph.astream_events(
            {"query": query, "history": formatted_history}, 
            version="v2"
        ):
            if await request.is_disconnected():
                logger.info("Client disconnected during streaming.")
                client_disconnected = True
                break
                
            kind = event["event"]
            tags = event.get("tags", [])
            
            # Emit metadata after the 'retrieve' node finishes
            if kind == "on_chain_end" and event["name"] == "retrieve":
                output = event["data"].get("output", {})
                if isinstance(output, dict) and "documents" in output and not metadata_sent:
                    documents = output["documents"]
                    philosophers_meta = []
                    for doc in documents:
                        meta = doc.get('metadata')
                        if meta not in philosophers_meta:
                            philosophers_meta.append(meta)
                            
                    if not documents:
                        # No documents found, we can still send an empty metadata
                        pass
                        
                    metadata_event = {
                        "philosophers": philosophers_meta
                    }
                    yield {"event": "metadata", "data": json.dumps(metadata_event, ensure_ascii=False)}
                    metadata_sent = True
                    await asyncio.sleep(0.1)
            
            # Watch for final generation streaming
            elif kind == "on_chat_model_stream" and "final_generation" in tags:
                chunk = event["data"]["chunk"].content
                if isinstance(chunk, str) and chunk:
                    chunk_count += 1
                    full_answer += chunk
                    chunk_clean = chunk.replace("\n", "\\n")
                    yield {"event": "content", "data": chunk_clean}
                    
            elif kind == "on_chain_end":
                # Debug logging to identify the correct event name if needed
                # logger.debug(f"Chain end: {event['name']}")
                
                # Check if this is the final output of the graph
                output = event["data"].get("output", {})
                if isinstance(output, dict) and ("documents" in output or "reformulated_query" in output):
                    final_state = output
                
        if chunk_count == 0 and not full_answer:
            # Check if graph final state already has an answer (e.g. from generate node)
            # that was not streamed for some reason.
            full_answer = str(final_state.get("answer") or "")
            if full_answer:
                yield {"event": "content", "data": full_answer.replace("\n", "\\n")}
                chunk_count = 1
            else:
                logger.warning("LLM returned 0 chunks and no final answer found.")
                yield {"event": "content", "data": "철학자는 난색을 표하며 서적을 뒤적거립니다. 대신 철학자가 답변을 해줄 만한 다른 질문은 없을까요?"}
            
        logger.info(f"Stream finished. Total chunks: {chunk_count}, Time: {time.perf_counter() - t0:.2f}s")
        
        # evaluation background task
        if not client_disconnected and background_tasks and final_state:
            from app.services.evaluation import evaluate_and_log
            contexts = [d["content"] for d in final_state.get("documents", [])]
            logger.info("Scheduling background evaluation task...")
            background_tasks.add_task(
                evaluate_and_log,
                query=query,
                reformulated_query=final_state.get("reformulated_query", ""),
                contexts=contexts,
                answer=full_answer,
                context_relevance=1.0 if final_state.get("is_relevant") else 0.0
            )
        else:
            logger.warning(f"Skipping evaluation. final_state_exists: {bool(final_state)}")

    except Exception:
        logger.exception("Failed while streaming LangGraph response")
        yield {"event": "error", "data": "오늘은 철학자도 사색의 시간이 필요하답니다. 내일 다시 지혜를 나누러 올게요."}
        return

from app.core.auth import get_current_user

@router.get("/eval-logs")
async def get_eval_logs(user: dict = Depends(get_current_user)):
    """
    Fetch the latest evaluation logs from Supabase.
    """
    try:
        from app.services.database import get_client
        res = get_client().table("eval_logs").select("*").order("created_at", desc=True).limit(50).execute()
        return res.data
    except Exception as e:
        logger.exception("Failed to fetch evaluation logs from database")
        from fastapi import HTTPException
        raise HTTPException(
            status_code=500, 
            detail="Failed to fetch evaluation logs"
        ) from e

@router.post("")
@limiter.limit("5/minute")
async def chat_endpoint(request: Request, chat_request: ChatRequest, background_tasks: BackgroundTasks):
    """
    Endpoint for accepting chat queries and returning a text/event-stream response.
    """
    return EventSourceResponse(generate_chat_events(request, chat_request.query, chat_request.history, background_tasks))

@router.post("/title")
@limiter.limit("10/minute")
async def chat_title_endpoint(request: Request, title_request: TitleRequest):
    """
    Endpoint for generating a short chat room title based on the first user query.
    """
    from app.services.llm import generate_chat_title_async
    
    query = title_request.query.strip()
    if not query:
        return {"title": DEFAULT_CHAT_TITLE}

    t_start = time.perf_counter()
    try:
        title = await asyncio.wait_for(generate_chat_title_async(query), timeout=CHAT_TIMEOUT)
        # Handle case where LLM returns something too long or with quotes
        title = title.replace('"', '').replace("'", "").strip()
        if not title:
            return {"title": DEFAULT_CHAT_TITLE}
        MAX_TITLE_LEN = 20
        ELLIPSIS = "..."
        if len(title) > MAX_TITLE_LEN:
            title = title[: MAX_TITLE_LEN - len(ELLIPSIS)] + ELLIPSIS
        return {"title": title}
    except asyncio.TimeoutError:
        logger.warning(f"Timeout generating chat title after {time.perf_counter() - t_start:.2f}s")
        return {"title": DEFAULT_CHAT_TITLE}
    except Exception:
        logger.exception("Failed to generate chat title")
        return {"title": DEFAULT_CHAT_TITLE}
