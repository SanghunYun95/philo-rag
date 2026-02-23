import os
import sys
import json
import urllib.request
import argparse
from typing import List, Dict

# Ensure we can import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.config import settings
from app.services.embedding import embedding_service
from app.services.database import supabase_client
from langchain.text_splitter import RecursiveCharacterTextSplitter

def fetch_aladin_metadata(title: str, author: str) -> Dict:
    """
    Dummy function for Aladin Open API.
    Aims to map English original titles to Korean translation book info.
    Replace with actual HTTP requests to Aladin API.
    """
    # Important: Fetching bookstore API here at ingestion time avoids SPOF at runtime
    api_key = settings.ALADIN_API_KEY
    if not api_key:
        print("Warning: ALADIN_API_KEY not set. Using mock metadata.")
        return {
            "title": f"Korean Translation of {title}",
            "cover_url": "https://image.aladin.co.kr/product/dummy",
            "link": "https://www.aladin.co.kr/dummy-link"
        }
        
    # Example logic (needs actual implementation depending on Aladin's API specs):
    # url = f"http://www.aladin.co.kr/ttb/api/ItemSearch.aspx?ttbkey={api_key}&Query={title}&QueryType=Title&SearchTarget=Book&output=js&Version=20131101"
    # Execute request and parse response...
    return {
        "title": f"Korean Translation of {title}",
        "cover_url": "https://image.aladin.co.kr/product/dummy",
        "link": "https://www.aladin.co.kr/dummy-link"
    }

def ingest_document(text: str, philosopher: str, school: str, book_title: str):
    """
    Chunks text, fetches metadata, generates embeddings, and upserts to Supabase.
    """
    print(f"Starting ingestion for {philosopher} - {book_title}")
    
    # 1. Fetch metadata (Phase 1, Step 2)
    book_info = fetch_aladin_metadata(book_title, philosopher)
    
    metadata = {
        "id": philosopher.lower().replace(" ", "_"),
        "school": school,
        "scholar": philosopher,
        "book_info": book_info
    }
    
    # 2. Chunk text (Phase 1, Step 3)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        is_separator_regex=False,
    )
    chunks = text_splitter.split_text(text)
    print(f"Generated {len(chunks)} chunks.")
    
    # 3. Embed & Upsert (Phase 1, Steps 4 & 5)
    for i, chunk in enumerate(chunks):
        embedding = embedding_service.generate_embedding(chunk)
        
        data, count = supabase_client.table('documents').insert({
            "content": chunk,
            "embedding": embedding,
            "metadata": metadata
        }).execute()
        
    print(f"Successfully ingrained {len(chunks)} chunks to Supabase.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest philosophical texts into Supabase")
    parser.add_argument("--file", type=str, required=True, help="Path to text file")
    parser.add_argument("--philosopher", type=str, required=True, help="Philosopher name")
    parser.add_argument("--school", type=str, required=True, help="School of thought")
    parser.add_argument("--title", type=str, required=True, help="Original Book Title")
    
    args = parser.parse_args()
    
    with open(args.file, 'r', encoding='utf-8') as f:
        text = f.read()
        
    ingest_document(text, args.philosopher, args.school, args.title)
