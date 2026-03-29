import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Compute repo root relative to this script
repo_root = Path(__file__).resolve().parent.parent
backend_path = repo_root / "backend"

# Add backend to path and load env from repo root
if str(backend_path) not in sys.path:
    sys.path.append(str(backend_path))
    
load_dotenv(dotenv_path=repo_root / ".env")

from app.services.database import get_client

def test_supabase():
    """Verify database connection with minimal data exposure."""
    try:
        db = get_client()
        # Query only non-sensitive columns for verification
        response = db.table("eval_logs").select("id, created_at").limit(1).execute()
        
        if response.data:
            print("Successfully connected to Supabase and read from eval_logs.")
            print(f"Verified {len(response.data)} record(s). Latest ID: {response.data[0]['id']}")
        else:
            print("Successfully connected to Supabase, but eval_logs table is empty.")
            
    except Exception as e:
        print(f"Error connecting to Supabase or reading from eval_logs: {e}")

if __name__ == "__main__":
    test_supabase()
