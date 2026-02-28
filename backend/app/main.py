from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import chat

app = FastAPI(
    title="PhiloRAG API",
    description="Backend API for PhiloRAG chatbot system",
    version="1.0.0",
)

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
