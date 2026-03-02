import pytest
from app.api.routes.chat import ChatRequest

def test_chat_request_accepts_history():
    """Test that ChatRequest model correctly parses history."""
    payload = {
        "query": "What is virtue?",
        "history": [
            {"role": "user", "content": "Hello"},
            {"role": "ai", "content": "How can I help you today?"}
        ]
    }
    
    request = ChatRequest(**payload)
    assert request.query == "What is virtue?"
    assert len(request.history) == 2
    assert request.history[0]["role"] == "user"
    assert request.history[1]["content"] == "How can I help you today?"

def test_chat_request_empty_history_default():
    """Test that ChatRequest model defaults to empty history."""
    payload = {"query": "What is virtue?"}
    
    request = ChatRequest(**payload)
    assert request.query == "What is virtue?"
    assert request.history == []
