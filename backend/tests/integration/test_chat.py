import pytest
from httpx import AsyncClient, ASGITransport
import asyncio
from app.main import app
from app.api.routes.chat import ChatRequest

@pytest.mark.asyncio
async def test_chat_rate_limiting():
    """Test that the chat endpoint correctly limits requests to 5 per minute."""
    
    # We will use the ASGITransport to test the FastAPI app directly
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # Define a unique client IP for this test to avoid interfering with other tests
        headers = {"X-Forwarded-For": "192.168.1.100"}
        
        # Send 5 requests which should succeed
        for _ in range(5):
            response = await ac.post("/api/v1/chat", json={"query": "Test"}, headers=headers)
            # Since the endpoint is streaming, we just need to ensure it's not a 429
            assert response.status_code == 200
            
        # The 6th request should fail with 429 Too Many Requests
        response = await ac.post("/api/v1/chat", json={"query": "Test"}, headers=headers)
        assert response.status_code == 429
