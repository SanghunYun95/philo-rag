from sentence_transformers import SentenceTransformer

# Load a pre-trained HuggingFace model for generating embeddings.
# all-MiniLM-L6-v2 is a good balance between speed and performance (384 dims).
# If 1536 dims is strictly required to match existing pgvector tables or 
# another embedding model config, use a compatible model or pad vectors.
# For demonstration and efficiency, we use all-MiniLM-L6-v2.

MODEL_NAME = 'all-MiniLM-L6-v2' 

class EmbeddingService:
    def __init__(self):
        # The model is loaded into memory when the service is instantiated.
        # This occurs on application startup if instantiated globally.
        self.model = SentenceTransformer(MODEL_NAME)
        
    def generate_embedding(self, text: str) -> list[float]:
        """
        Generates a vector embedding for the given text.
        """
        embedding = self.model.encode(text)
        # Convert numpy array to list of floats for pgvector/JSON
        return embedding.tolist()

# Singleton instance
embedding_service = EmbeddingService()
