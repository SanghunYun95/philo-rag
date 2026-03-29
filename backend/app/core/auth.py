import secrets
from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from app.core.config import settings

# This is a simple API key authentication for the dashboard logs.
# For production, consider using a full OAuth2/Supabase Auth system.
API_KEY_NAME = "x-admin-key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def get_current_user(api_key: str = Depends(api_key_header)):
    """
    Validates the admin secret key from request headers using constant-time comparison.
    """
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Admin Secret Key",
        )
    
    # Secure constant-time comparison to prevent timing attacks
    is_valid = secrets.compare_digest(api_key, settings.ADMIN_SECRET_KEY)
    
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Admin Secret Key",
        )
    return {"user": "admin"}

