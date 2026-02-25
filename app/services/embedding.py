from langchain_google_genai import GoogleGenerativeAIEmbeddings
from app.core.config import settings

# Google's text-embedding-004 is a powerful model.
# By default it produces 768 dimensions.
# Since the database was initialized with 1536 dimensions, 
# we should ideally match it or update the database schema.
# For now, we'll use Gemini embeddings and recommend a schema update if necessary.

MODEL_NAME = "models/gemini-embedding-001"

class EmbeddingService:
    def __init__(self):
        # Using Gemini API for embeddings avoids the heavy local torch dependency
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model=MODEL_NAME,
            google_api_key=settings.GEMINI_API_KEY
        )
        
    def generate_embedding(self, text: str) -> list[float]:
        """
        Generates a vector embedding for the given text using Gemini.
        """
        # The invoke method returns a list of floats
        return self.embeddings.embed_query(text)

# Singleton instance
embedding_service = EmbeddingService()
