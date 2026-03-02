from fastapi.testclient import TestClient
import pytest
from app.main import app
from unittest.mock import patch

@patch("app.api.routes.chat.generate_chat_events")
def test_chat_rate_limiting(mock_events):
    """Test that the chat endpoint correctly limits requests to 5 per minute."""
    
    # Mock event generator to bypass ML initializations and remote calls
    async def mock_generator(*_args, **_kwargs):
        yield "data: ok\n\n"
    def _mock_events_factory(*_args, **_kwargs):
        return mock_generator()
    mock_events.side_effect = _mock_events_factory
    
    # We will use the synchronous TestClient to avoid asyncio event loop leaking from SSE Streams
    with TestClient(app) as client:
        # Define a unique client IP for this test to avoid interfering with other tests
        headers = {"X-Forwarded-For": "192.168.1.100"}
        
        # Send 5 requests which should succeed
        for _ in range(5):
            # We use stream matching to verify successful request dispatching
            with client.stream("POST", "/api/v1/chat", json={"query": "Test"}, headers=headers) as response:
                assert response.status_code == 200
            
        # The 6th request should fail with 429 Too Many Requests
        response = client.post("/api/v1/chat", json={"query": "Test"}, headers=headers)
        assert response.status_code == 429
