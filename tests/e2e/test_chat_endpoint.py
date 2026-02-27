import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

@patch("app.api.routes.chat.embedding_service.generate_embedding")
@patch("app.api.routes.chat.supabase_client.rpc")
@patch("app.api.routes.chat.get_english_translation")
@patch("app.api.routes.chat.get_response_stream")
def test_chat_endpoint_success(mock_stream, mock_translate, mock_rpc, mock_embed):
    # Setup mocks
    mock_translate.return_value = "What is life?"
    mock_embed.return_value = [0.1] * 384
    
    # Mock supabase response
    mock_execute = MagicMock()
    mock_execute.execute.return_value.data = [
        {"content": "Life is suffering", "metadata": {"author": "Schopenhauer"}}
    ]
    mock_rpc.return_value = mock_execute
    
    # Mock LLM stream generator
    mock_stream.return_value = (chunk for chunk in ["인생은", " ", "고통입니다."])
    
    # Call the actual endpoint with Fastapi test client
    # Since it's SSE, we stream the response
    with client.stream("POST", "/api/v1/chat", json={"query": "인생이란?"}) as response:
        assert response.status_code == 200
        assert "text/event-stream" in response.headers["content-type"]
        
        # Read the stream text block
        text = response.read().decode("utf-8")
        
        # The EventSourceResponse from sse_starlette outputs like:
        # event: metadata\r\ndata: {"philosophers": [{"author": "Schopenhauer"}]}\r\n\r\n
        assert "event: metadata" in text
        assert "Schopenhauer" in text
        assert "event: content" in text
        assert "data: 인생은" in text
        assert "data:  " in text
        assert "data: 고통입니다." in text

def test_chat_endpoint_missing_query():
    # Should fail validation (422 Unprocessable Entity) because query is required
    response = client.post("/api/v1/chat", json={})
    assert response.status_code == 422
