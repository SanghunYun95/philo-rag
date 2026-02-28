from supabase import create_client, Client
from app.core.config import settings

def get_supabase_client() -> Client:
    """
    Returns a configured Supabase client using the URL and Service Key.
    The Service Key is used to bypass RLS for administrative backend tasks 
    like upserting documents or fetching metadata securely.
    """
    supabase_url = settings.SUPABASE_URL or "http://localhost:8000"
    supabase_key = settings.SUPABASE_SERVICE_KEY or "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSJ9.1234567890"
    return create_client(supabase_url, supabase_key)

# Initialize a global client to be reused
supabase_client = get_supabase_client()
