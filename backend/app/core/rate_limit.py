from slowapi import Limiter
from slowapi.util import get_remote_address
from starlette.requests import Request

def get_real_client_ip(request: Request) -> str:
    """Get real client IP considering X-Forwarded-For header in a proxy environment."""
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return get_remote_address(request)

limiter = Limiter(key_func=get_real_client_ip)
