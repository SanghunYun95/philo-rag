import threading
import logging
from langchain_huggingface import HuggingFaceEndpointEmbeddings
from app.core.config import settings

logger = logging.getLogger(__name__)


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
EXPECTED_EMBEDDING_DIM = 384

class EmbeddingService:
    def __init__(self):
        self._embeddings = None
        self._lock = threading.Lock()
        
    @property
    def embeddings(self):
        if self._embeddings is None:
            with self._lock:
                if self._embeddings is None:
                    logger.info("Using HuggingFace Inference API for embedding model: %s", MODEL_NAME)
                    if not settings.HUGGINGFACEHUB_API_TOKEN:
                        logger.warning("HUGGINGFACEHUB_API_TOKEN is not set. The Inference API might fail if heavily rate-limited.")
                    self._embeddings = HuggingFaceEndpointEmbeddings(
                        model=MODEL_NAME,
                        task="feature-extraction",
                        huggingfacehub_api_token=settings.HUGGINGFACEHUB_API_TOKEN
                    )
                    logger.info("HuggingFace Inference API configured successfully.")
        return self._embeddings
        
    def _validate_embedding_dimension(self, embedding: list[float]) -> None:
        if len(embedding) != EXPECTED_EMBEDDING_DIM:
            raise ValueError(
                f"Unexpected embedding dimension: {len(embedding)} (expected {EXPECTED_EMBEDDING_DIM})"
            )

    def generate_embedding(self, text: str) -> list[float]:
        """
        Generates a vector embedding for the given text using the HuggingFace model.
        Returns a list of 384 floats matching the model's actual vector length.
        """
        # The embed_query method returns a list of floats
        embedding = self.embeddings.embed_query(text)
        self._validate_embedding_dimension(embedding)
        return embedding

    async def agenerate_embedding(self, text: str) -> list[float]:
        """Async version of vector embedding generation."""
        embedding = await self.embeddings.aembed_query(text)
        self._validate_embedding_dimension(embedding)
        return embedding

# Singleton instance
embedding_service = EmbeddingService()
