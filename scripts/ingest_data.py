import os
import sys
import json
import uuid
import urllib.request
import argparse
import concurrent.futures
from typing import List, Dict

# Ensure we can import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.config import settings
from app.services.embedding import embedding_service
from app.services.database import supabase_client
from langchain.text_splitter import RecursiveCharacterTextSplitter

class IngestionError(Exception):
    """Raised when data ingestion fails."""
    def __init__(self, failed_batches):
        self.failed_batches = failed_batches
        super().__init__(f"Ingestion incomplete. Failed batches: {failed_batches}")

def fetch_aladin_metadata(title: str, author: str) -> Dict:
    """
    Dummy function for Aladin Open API.
    Aims to map English original titles to Korean translation book info.
    Replace with actual HTTP requests to Aladin API.
    """
    api_key = settings.ALADIN_API_KEY
    if not api_key:
        print("Warning: ALADIN_API_KEY not set. Using mock metadata.")
        return {
            "title": f"Korean Translation of {title}",
            "cover_url": "https://image.aladin.co.kr/product/dummy",
            "link": "https://www.aladin.co.kr/dummy-link"
        }
        
    return {
        "title": f"Korean Translation of {title}",
        "cover_url": "https://image.aladin.co.kr/product/dummy",
        "link": "https://www.aladin.co.kr/dummy-link"
    }
UUID_NAMESPACE = uuid.UUID("6f0bdf73-9cc8-4e34-a302-a12037f0ac6d")

def generate_deterministic_uuid(seed_text: str) -> str:
    """Generates a consistent UUID based on the input text to ensure idempotency."""
    return str(uuid.uuid5(UUID_NAMESPACE, seed_text))

def strip_gutenberg_boilerplate(text: str) -> str:
    """Removes Project Gutenberg START and END identifiers from the text."""
    start_marker = "*** START OF THE PROJECT GUTENBERG EBOOK"
    end_marker = "*** END OF THE PROJECT GUTENBERG EBOOK"
    
    start_idx = text.upper().find(start_marker)
    if start_idx != -1:
        # Move past the marker line
        newline_idx = text.find("\n", start_idx)
        if newline_idx != -1:
            text = text[newline_idx+1:]
            
    end_idx = text.upper().find(end_marker)
    if end_idx != -1:
        text = text[:end_idx]
        
    return text

def generate_embedding_with_retry(text: str, max_retries: int = 3):
    """Wrapper to handle rate limiting and retries for the embedding API."""
    import time
    for attempt in range(max_retries):
        try:
            return embedding_service.generate_embedding(text)
        except Exception as exc:
            if attempt < max_retries - 1:
                sleep_time = 2 ** (attempt + 1)
                print(f"Embedding API exception: {exc}. Retrying in {sleep_time}s...")
                time.sleep(sleep_time)
            else:
                print(f"Failed to generate embedding after {max_retries} attempts.")
                raise exc

def ingest_document(text: str, philosopher: str, school: str, book_title: str, limit: int = None):
    """
    Chunks text, fetches metadata, generates embeddings via multiprocessing,
    and upserts to Supabase in batches with idempotency.
    """
    print(f"Starting ingestion for {philosopher} - {book_title}")
    
    # 1. Fetch metadata
    book_info = fetch_aladin_metadata(book_title, philosopher)
    
    metadata = {
        "id": philosopher.lower().replace(" ", "_"),
        "school": school,
        "scholar": philosopher,
        "book_info": book_info
    }
    
    # 2. Chunk text (Meaning units + Metadata Injection + Boilerplate Stripping)
    cleaned_text = strip_gutenberg_boilerplate(text)
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", " ", ""],
        length_function=len,
        is_separator_regex=False,
    )
    chunks = text_splitter.split_text(cleaned_text)
    
    if limit is not None and limit > 0:
        chunks = chunks[:limit]
        print(f"Limiting to {limit} chunks for testing.")
        
    print(f"Generated {len(chunks)} chunks.")
    
    # 3. Check existing chunks in DB to prevent re-embedding (Resume functionality)
    existing_indices = set()
    try:
        # Fetching all chunks for this specific book to skip them
        res = supabase_client.table('documents') \
            .select('metadata') \
            .eq("metadata->>'scholar'", philosopher) \
            .eq("metadata->'book_info'->>'title'", book_info.get('title')) \
            .execute()
        
        # Filter by title in python to avoid complex JSONB querying issues
        for row in res.data:
            meta = row.get('metadata', {})
            # Compare with the title saved in DB (from fetch_aladin_metadata)
            if meta.get('book_info', {}).get('title') == book_info.get('title'):
                existing_indices.add(meta.get('chunk_index'))
                
        if existing_indices:
            print(f"Found {len(existing_indices)} existing chunks for this book. They will be skipped.")
    except Exception as e:
        print(f"Could not check existing chunks: {e}")

    # 4. Batch Process: Chunk -> Embed -> Upsert Loop
    BATCH_SIZE = 100
    failed_batches = []
    
    for i in range(0, len(chunks), BATCH_SIZE):
        batch_chunks = chunks[i:i + BATCH_SIZE]
        batch_data = []
        
        # Inject metadata into content for better context
        enriched_chunks = []
        for j, chunk in enumerate(batch_chunks):
            chunk_idx = i + j
            if chunk_idx in existing_indices:
                continue # Skip already processed chunks to save API quota
                
            # Prepending author and title preserves context inside the chunk for the embedding model
            enriched_content = f"Title: {book_title}\nAuthor: {philosopher}\n\n{chunk}"
            enriched_chunks.append((chunk_idx, enriched_content, chunk))
            
        if not enriched_chunks:
            continue # All chunks in this batch were already processed
            
        print(f"Processing batch {i//BATCH_SIZE + 1}/{(len(chunks)-1)//BATCH_SIZE + 1} ({len(enriched_chunks)} new chunks)...")
        
        # Multiprocessing (Thread pool for I/O bound embedding API calls)
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            future_to_chunk = {
                executor.submit(generate_embedding_with_retry, ec): (idx, ec, oc) 
                for idx, ec, oc in enriched_chunks
            }
            
            for future in concurrent.futures.as_completed(future_to_chunk):
                idx, enriched_content, original_content = future_to_chunk[future]
                
                try:
                    embedding = future.result()
                    
                    # Idempotency: Create deterministic ID based on content and position
                    unique_id = generate_deterministic_uuid(f"{philosopher}_{book_title}_{idx}_{original_content}")
                    
                    batch_data.append({
                        "id": unique_id,
                        "content": enriched_content,         # Store the text with injected metadata
                        "embedding": embedding,
                        "metadata": {
                            **metadata,
                            "chunk_index": idx
                        }
                    })
                except Exception as exc:
                    print(f"Chunk {idx} completely failed: {exc}")
                    
        # Upsert the batch to Supabase
        if batch_data:
            try:
                # 'upsert' overwrites based on the unique UUID primary key constraint
                supabase_client.table('documents').upsert(batch_data).execute()
                print(f"✅ Successfully upserted {len(batch_data)} chunks to Supabase.")
            except Exception as e:
                print(f"❌ Error upserting batch: {e}")
                failed_batches.append((i // BATCH_SIZE + 1, str(e)))

    if failed_batches:
        raise IngestionError(failed_batches)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest philosophical texts into Supabase")
    parser.add_argument("--file", type=str, required=True, help="Path to text file")
    parser.add_argument("--philosopher", type=str, required=True, help="Philosopher name")
    parser.add_argument("--school", type=str, required=True, help="School of thought")
    parser.add_argument("--title", type=str, required=True, help="Original Book Title")
    parser.add_argument("--limit", type=int, default=None, help="Limit the number of chunks to process (for testing)")
    
    args = parser.parse_args()
    
    with open(args.file, 'r', encoding='utf-8') as f:
        text = f.read()
        
    ingest_document(text, args.philosopher, args.school, args.title, args.limit)
