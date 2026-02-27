import os
import sys

# Ensure we can import app modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.database import supabase_client
import uuid

def verify_and_clear():
    print("Clearing 'documents' table...")
    # Delete all rows
    try:
        total_deleted = 0
        while True:
            # Fetch up to 100 IDs to delete
            res = supabase_client.table("documents").select("id").limit(100).execute()
            if not res.data:
                break
            ids = [r['id'] for r in res.data]
            
            # Batch delete
            del_res = supabase_client.table("documents").delete().in_("id", ids).execute()
            total_deleted += len(ids)
            print(f"Deleted batch of {len(ids)} rows. Total deleted so far: {total_deleted}")
            
        print(f"Cleared {total_deleted} rows from 'documents'.")
    except Exception as e:
        print(f"Error clearing table: {e}")
        return

    print("Verifying vector dimension (384)...")
    # Generate a dummy 384-dimensional vector
    dummy_vector = [0.0] * 384
    dummy_id = str(uuid.uuid4())
    
    try:
        res = supabase_client.table("documents").insert({
            "id": dummy_id,
            "content": "test verification",
            "embedding": dummy_vector,
            "metadata": {"type": "verification"}
        }).execute()
        print("Success: Vector dimension 384 is accepted by the database.")
        
        # Clean up the dummy row
        supabase_client.table("documents").delete().eq("id", dummy_id).execute()
        print("Verification complete and database is clean.")
    except Exception as e:
        print("Failed to insert 384-dimensional vector. The schema might not be updated to 384.")
        print(f"Error details: {e}")

if __name__ == "__main__":
    verify_and_clear()
