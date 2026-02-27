from langchain_community.embeddings.fastembed import FastEmbedEmbeddings

# FastEmbed provides the exact same model (all-MiniLM-L6-v2) but via ONNX,
# bypassing the need for PyTorch and Microsoft C++ Redistributables on Windows.
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

class EmbeddingService:
    def __init__(self):
        self._embeddings = None
        
    @property
    def embeddings(self):
        if self._embeddings is None:
            print(f"Loading local embedding model: {MODEL_NAME} (FastEmbed)...")
            self._embeddings = FastEmbedEmbeddings(
                model_name=MODEL_NAME,
                max_length=512
            )
            print("Local embedding model loaded successfully.")
        return self._embeddings
        
    def generate_embedding(self, text: str) -> list[float]:
        """
        Generates a vector embedding for the given text using the FastEmbed model.
        Returns a list of 384 floats.
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
