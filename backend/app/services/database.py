from supabase import create_client, Client
from app.core.config import settings

def get_supabase_client() -> Client:
    """
    Returns a configured Supabase client using the URL and Service Key.
    The Service Key is used to bypass RLS for administrative backend tasks 
    like upserting documents or fetching metadata securely.
    """
    supabase_url = settings.SUPABASE_URL
    supabase_key = settings.SUPABASE_SERVICE_KEY
    if not supabase_url or not supabase_key:
        raise RuntimeError("SUPABASE_URL and SUPABASE_SERVICE_KEY must be configured")
    return create_client(supabase_url, supabase_key)

# Initialize a global client to be reused
supabase_client = get_supabase_client()
