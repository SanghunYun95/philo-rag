import pytest
from unittest.mock import patch, MagicMock
from app.api.routes.chat import generate_chat_events
from app.services.embedding import embedding_service

# We are testing the integration of embedding and database retrieval logic that happens within generate_chat_events
# Specifically, we want to mock just the supabase client and ensure it gets called with the embedded vector

@pytest.mark.asyncio
async def test_supabase_match_integration():
    # 1. We mock the embedding service to return a dummy vector
    with patch("app.api.routes.chat.embedding_service.generate_embedding") as mock_embed, \
         patch("app.api.routes.chat.supabase_client.rpc") as mock_rpc, \
         patch("app.api.routes.chat.get_english_translation") as mock_translate, \
         patch("app.api.routes.chat.get_response_stream") as mock_stream:
         
        mock_translate.return_value = "English Question"
        mock_embed.return_value = [0.1, 0.2, 0.3]
        
        # Mock Supabase RPC response chain: .rpc().execute().data
        mock_execute = MagicMock()
        mock_execute.execute.return_value.data = [
            {"content": "Philosophy is life", "metadata": {"author": "Socrates"}}
        ]
        mock_rpc.return_value = mock_execute
        
        # Mock LLM stream
        mock_stream.return_value = (chunk for chunk in ["답변", "입니다"])
        
        # We need a mock request for the SSE loop
        from unittest.mock import AsyncMock
        mock_request = MagicMock()
        mock_request.is_disconnected = AsyncMock(return_value=False)
        
        generator = generate_chat_events(mock_request, "안녕")
        
        events = []
        async for event in generator:
            events.append(event)
            
        # Assertions
        mock_translate.assert_called_once_with("안녕")
        mock_embed.assert_called_once_with("English Question")
        
        # Important: Verify Supabase RPC was called with the exact vector from Embedding Service
        mock_rpc.assert_called_once_with(
            'match_documents', 
            {'query_embedding': [0.1, 0.2, 0.3], 'match_count': 3}
        )
        
        # Verify event stream structure
        assert len(events) == 3 # metadata + "답변" + "입니다"
        assert events[0]["event"] == "metadata"
        assert events[1]["event"] == "content"
        assert events[1]["data"] == "답변"
        assert events[2]["data"] == "입니다"
