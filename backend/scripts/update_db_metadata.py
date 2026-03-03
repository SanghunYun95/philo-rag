import os
import sys
import json
import asyncio
from pathlib import Path
from dotenv import load_dotenv

backend_dir = Path(__file__).resolve().parents[1]
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

env_path = backend_dir.parent / ".env"
load_dotenv(dotenv_path=env_path)

from app.services.database import get_client

# Load mapping data
MAPPING_FILE = backend_dir / "data" / "books_mapping.json"

def update_database():
    print(f"Loading mapping from {MAPPING_FILE}")
    if not MAPPING_FILE.exists():
        print("Mapping file not found.")
        return

    with open(MAPPING_FILE, "r", encoding="utf-8") as f:
        try:
            mapping_data = json.load(f)
        except Exception as e:
            print(f"Error reading JSON: {e}")
            return
            
    print(f"Found {len(mapping_data)} mapping entries.")

    supabase = get_client()

    success_count = 0
    error_count = 0

    print("Fetching all document metadata ids to match locally...")
    # Fetching all chunks to match metadata in memory to save DB query overhead/complexity.
    # We only need id and metadata explicitly.
    try:
        # Since we might have many records, we paginate or fetch all
        # Assuming < 10000 chunks for 100 books. Let's fetch all in one go or paginate.
        all_docs = []
        limit = 1000
        offset = 0
        while True:
            res = supabase.table("documents").select("id, metadata").range(offset, offset + limit - 1).execute()
            all_docs.extend(res.data)
            if len(res.data) < limit:
                break
            offset += limit
        print(f"Total document chunks retrieved: {len(all_docs)}")
        
    except Exception as e:
        print(f"Error fetching from supabase: {e}")
        return

    print("\nStarting batch updates...")
    
    # Pre-process mapping data into a dictionary for quick lookup by 'title_to_match'
    mapping_dict = {}
    for book in mapping_data:
        original_file = book.get("original_file", "")
        # Parse filename exactly as ingest_all_data.py did to recreate the title.
        name_without_ext = Path(original_file).stem
        parts = name_without_ext.rsplit(" by ", 1)
        if len(parts) == 2:
            title = parts[0].strip()
        else:
            title = name_without_ext
            
        # ingest_data.py stores this specific mock title in the DB:
        title_to_match = f"Korean Translation of {title}"
        mapping_dict[title_to_match] = book

    updates_to_make = []

    if all_docs:
        print("Sample metadata from DB:", all_docs[0]['metadata'])

    for doc in all_docs:
        doc_id = doc['id']
        metadata = doc['metadata']
        
        if not isinstance(metadata, dict):
            print(f"Skipping doc {doc_id}: metadata is not a dict")
            continue
        
        # The DB stores the title we want to match inside metadata->book_info->title
        db_title = metadata.get('book_info', {}).get('title', '')
        
        # Determine which mapping record matches this chunk's DB title
        matched_book = mapping_dict.get(db_title)
                
        if matched_book:
            kr_title = matched_book.get("translated_title", "")
            aladin = matched_book.get("aladin_data", {})
            thumbnail = aladin.get("thumbnail", "")
            link = aladin.get("link", "")
            
            # Check if we actually need to update
            if metadata.get("kr_title") != kr_title or metadata.get("thumbnail") != thumbnail or metadata.get("link") != link:
                metadata["kr_title"] = kr_title
                metadata["thumbnail"] = thumbnail
                metadata["link"] = link
                updates_to_make.append({"id": doc_id, "metadata": metadata})

    print(f"Determined {len(updates_to_make)} chunks need metadata updates.")

    # Batch update using concurrent updates
    if updates_to_make:
        import concurrent.futures
        from time import sleep

        def update_doc(doc):
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    supabase.table("documents").update({"metadata": doc["metadata"]}).eq("id", doc["id"]).execute()
                    return True
                except Exception as e:
                    if attempt < max_retries - 1:
                        sleep(0.5 * (attempt + 1))  # Exponential backoff
                        continue
                    print(f"Error updating {doc['id']}: {e}")
                    return False

        print(f"Starting concurrent updates with 10 workers for {len(updates_to_make)} rows...")
        processed = 0
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            for result in executor.map(update_doc, updates_to_make):
                processed += 1
                if result:
                    success_count += 1
                else:
                    error_count += 1
                    
                if processed % 1000 == 0:
                    print(f"Processed {processed}/{len(updates_to_make)}...")
                    
    print(f"\nUpdate complete! Success: {success_count}, Errors: {error_count}")

if __name__ == "__main__":
    update_database()
