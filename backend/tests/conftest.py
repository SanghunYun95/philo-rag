import os
import pytest
import asyncio

@pytest.fixture(autouse=True)
def mock_env_vars():
    """Set dummy environment variables for tests to prevent import errors."""
    os.environ["GEMINI_API_KEY"] = "dummy_test_key"
    os.environ["SUPABASE_URL"] = "http://localhost:8000"
    os.environ["SUPABASE_SERVICE_KEY"] = "dummy_service_key"

@pytest.fixture(scope="session")
def event_loop():
    """Create a single event loop instance shared across the entire test session.
    Scoped to session to prevent global client implementations (e.g. Supabase Python client) 
    from binding `asyncio.locks.Event` instances to closed function-scoped event loops."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(autouse=True)
def reset_sse_starlette_appstatus():
    """Reset the global AppStatus event in sse-starlette to prevent event loop leakage between tests."""
    import sse_starlette.sse
    sse_starlette.sse.AppStatus.should_exit_event = None
    yield

@pytest.fixture(autouse=True)
def reset_rate_limiter_storage():
    """Reset the rate limiter's storage between tests so that asyncio Locks are not shared across TestClient event loops."""
    from app.core.rate_limit import limiter
    from limits.storage import MemoryStorage
    
    # limits 3.x MemoryStorage creates an asyncio.Lock internally. 
    # Resetting it forces re-bind to current test context.
    limiter._storage = MemoryStorage()
    yield
