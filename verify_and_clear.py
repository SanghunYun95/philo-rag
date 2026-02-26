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
        # A hack to delete all rows is to use an inequality that is always true
        res = supabase_client.table("documents").delete().neq("id", "00000000-0000-0000-0000-000000000000").execute()
        print(f"Cleared {len(res.data)} rows from 'documents'.")
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
