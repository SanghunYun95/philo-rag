from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.api.routes import chat
from app.core.rate_limit import limiter
import asyncio
from contextlib import asynccontextmanager
import logging

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(_app: FastAPI):
    # Ensure all required environment variables are set before proceeding
    from app.core.config import validate_required_settings
    validate_required_settings()
    
    # Pre-load embedding model and LLM during startup
    # We offload these heavy initializations to a worker thread so as not to block the event loop.
    logger.info("Initializing AI models starting (async)...")
    from app.services.embedding import embedding_service
    from app.services.llm import get_llm
    
    # Offload HuggingFace downloads and LLM instantiation to threads
    await asyncio.gather(
        asyncio.to_thread(lambda: embedding_service.embeddings),
        asyncio.to_thread(get_llm)
    )
    logger.info("Model initialization complete.")
    
    try:
        yield
    finally:
        pass

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
    allow_origins=[
        "http://localhost:3000",
        "https://philo-rag.web.app",
        "https://philo-rag.firebaseapp.com",
        "https://philo-rag.vercel.app"
    ],
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
    # Since models are now pre-loaded sequentially during lifespan startup,
    # if the server is running and responding, it's ready.
    return {"status": "ready"}
