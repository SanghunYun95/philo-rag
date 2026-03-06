import threading
from supabase import create_client, Client, ClientOptions
from app.core.config import settings

SUPABASE_CONFIG_ERROR = "SUPABASE_URL and SUPABASE_SERVICE_KEY must be configured"

def _get_supabase_client() -> Client:
    """
    Returns a configured Supabase client using the URL and Service Key.
    The Service Key is used to bypass RLS for administrative backend tasks 
    like upserting documents or fetching metadata securely.
    """
    supabase_url = settings.SUPABASE_URL
    supabase_key = settings.SUPABASE_SERVICE_KEY
    if not supabase_url or not supabase_key:
        raise RuntimeError(SUPABASE_CONFIG_ERROR)
    
    options = ClientOptions(postgrest_client_timeout=30)
    return create_client(supabase_url, supabase_key, options=options)


_client_lock = threading.Lock()
# Lazy initialization for Supabase client
_supabase_client: Client | None = None

def get_client() -> Client:
    global _supabase_client
    if _supabase_client is None:
        with _client_lock:
            if _supabase_client is None:
                _supabase_client = _get_supabase_client()
    return _supabase_client
