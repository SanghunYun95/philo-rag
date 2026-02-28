import os
import sys

# Ensure we can import app modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.database import supabase_client

def check_progress():
    print("Querying Supabase to check ingestion progress...")
    try:
        res = supabase_client.table('documents').select('metadata').execute()
        
        books = {}
        for row in res.data:
            meta = row.get('metadata', {})
            title = meta.get('book_info', {}).get('title', 'Unknown Title')
            books[title] = books.get(title, 0) + 1
            
        print("\n--- Ingestion Progress ---")
        if not books:
            print("No documents found in the database.")
        else:
            for title, count in books.items():
                print(f"- {title}: {count} chunks")
            print(f"\nTotal Chunks: {len(res.data)}")
            print(f"Total Books Started: {len(books)}")
            
    except Exception as e:
        print(f"Error querying database: {e}")

if __name__ == "__main__":
    check_progress()
