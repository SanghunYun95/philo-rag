import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

@patch("app.services.embedding.EmbeddingService.agenerate_embedding")
@patch("app.api.routes.chat._search_documents")
@patch("app.services.llm.get_english_translation")
@patch("app.services.llm.get_response_stream_async")
def test_chat_endpoint_success(mock_stream, mock_translate, mock_search, mock_embed):
    # Setup mocks
    mock_translate.return_value = "What is life?"
    mock_embed.return_value = [0.1] * 384
    
    # Mock _search_documents response
    mock_response = MagicMock()
    mock_response.data = [
        {"content": "Life is suffering", "metadata": {"author": "Schopenhauer"}}
    ]
    mock_search.return_value = mock_response
    
    # Mock LLM stream generator
    async def mock_async_generator(*_args, **_kwargs):
        for chunk in ["인생은", " ", "고통입니다."]:
            yield chunk
    mock_stream.return_value = mock_async_generator()
    
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
