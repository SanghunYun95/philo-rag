import os
import sys
from dotenv import load_dotenv

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), "backend"))

load_dotenv()

from app.services.database import get_client

def test_supabase():
    try:
        db = get_client()
        # Try to fetch from eval_logs
        response = db.table("eval_logs").select("*").limit(1).execute()
        print("Successfully connected to Supabase and read from eval_logs.")
        print(f"Data found: {response.data}")
    except Exception as e:
        print(f"Error connecting to Supabase or reading from eval_logs: {e}")

if __name__ == "__main__":
    test_supabase()
