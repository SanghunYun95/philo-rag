import threading
import logging
from langchain_community.embeddings import HuggingFaceEmbeddings

logger = logging.getLogger(__name__)


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

class EmbeddingService:
    def __init__(self):
        self._embeddings = None
        self._lock = threading.Lock()
        
    @property
    def embeddings(self):
        if self._embeddings is None:
            with self._lock:
                if self._embeddings is None:
                    logger.info(f"Loading local embedding model: {MODEL_NAME} (HuggingFace)...")
                    self._embeddings = HuggingFaceEmbeddings(
                        model_name=MODEL_NAME,
                        model_kwargs={'device': 'cpu'},
                        encode_kwargs={'normalize_embeddings': True}
                    )
                    logger.info("Local embedding model loaded successfully.")
        return self._embeddings
        
    def generate_embedding(self, text: str) -> list[float]:
        """
        Generates a vector embedding for the given text using the HuggingFace model.
        Returns a list of 384 floats matching the model's actual vector length.
        """
        # The embed_query method returns a list of floats
        embedding = self.embeddings.embed_query(text)
        if len(embedding) != 384:
            raise ValueError(
                f"Unexpected embedding dimension: {len(embedding)} (expected 384)"
            )
        return embedding

# Singleton instance
embedding_service = EmbeddingService()
