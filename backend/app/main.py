from fastapi import FastAPI
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
        try:
            from app.services.embedding import embedding_service
            from app.services.llm import get_llm
            _ = embedding_service.embeddings
            _ = get_llm()
            logger.info("Pre-loading successful.")
        except Exception:
            logger.exception("Failed to pre-load models")
            raise

    # Run in a background thread to avoid blocking the Uvicorn port binding on Render
    asyncio.get_event_loop().run_in_executor(None, preload_models)
    yield

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
