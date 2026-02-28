import asyncio
import os
import sys

# add backend dir to path
sys.path.append(r"c:\Users\ysn65\Desktop\antigravity\philo-rag\backend")

from app.core.config import settings
from langchain_google_genai import GoogleGenerativeAIEmbeddings

def test():
    embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004", google_api_key=settings.GEMINI_API_KEY)
    vec = embeddings.embed_query("Hello world")
    print(f"Dimension: {len(vec)}")

if __name__ == "__main__":
    test()
