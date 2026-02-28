from supabase import create_client, Client
from app.core.config import settings

def get_supabase_client() -> Client:
    """
    Returns a configured Supabase client using the URL and Service Key.
    The Service Key is used to bypass RLS for administrative backend tasks 
    like upserting documents or fetching metadata securely.
    """
    if not settings.SUPABASE_URL or not settings.SUPABASE_SERVICE_KEY:
        raise ValueError("Supabase URL and Service Key must be set in environment variables.")
        
    return create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_KEY)

# Initialize a global client to be reused
supabase_client = get_supabase_client()
