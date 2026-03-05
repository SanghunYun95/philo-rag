from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.api.routes import chat
from app.core.rate_limit import limiter
from contextlib import asynccontextmanager
import logging

logger = logging.getLogger(__name__)

import asyncio

@asynccontextmanager
async def lifespan(_app: FastAPI):
    # Pre-load embedding model and LLM during startup in a background thread
    logger.info("Pre-loading models in background during startup...")
    
    def preload_models():
        from app.services.embedding import embedding_service
        from app.services.llm import get_llm
        _ = embedding_service.embeddings
        _ = get_llm()
        logger.info("Pre-loading successful.")

    # Run in a background thread to avoid blocking the Uvicorn port binding on Render
    preload_task = asyncio.create_task(asyncio.to_thread(preload_models))
    _app.state.preload_task = preload_task
    
    def _on_preload_done(task: asyncio.Task):
        try:
            if task.cancelled():
                logger.warning("Preload task was cancelled")
                return
            task.result()
        except Exception:
            logger.exception("Failed to pre-load models")
            
    preload_task.add_done_callback(_on_preload_done)
    try:
        yield
    finally:
        if not preload_task.done():
            try:
                # Use wait_for to shield and wait so we don't aggressively cancel a thread that might hang
                await asyncio.wait_for(asyncio.shield(preload_task), timeout=3.0)
            except asyncio.TimeoutError:
                logger.warning("Preload task did not finish before shutdown.")

app = FastAPI(
    title="PhiloRAG API",
    description="Backend API for PhiloRAG chatbot system",
    version="1.0.0",
    lifespan=lifespan,
)

# Register rate limiter
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat.router, prefix="/api/v1/chat", tags=["chat"])

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/ready")
async def readiness_check():
    preload_task = getattr(app.state, "preload_task", None)
    if preload_task is None or not preload_task.done():
        return JSONResponse({"status": "not_ready"}, status_code=503)
        
    if preload_task.cancelled():
        logger.warning("Preload task was cancelled during readiness check")
        return JSONResponse({"status": "failed"}, status_code=503)
        
    try:
        preload_task.result()  # re-raises if failed
        return {"status": "ready"}
    except Exception:
        logger.exception("Preload task failed during readiness check")
        return JSONResponse({"status": "failed"}, status_code=503)
