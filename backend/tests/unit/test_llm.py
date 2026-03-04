
import sys
import pytest
from pathlib import Path

# dynamically add backend root dir to path
backend_dir = Path(__file__).resolve().parents[2]
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

import os

@pytest.fixture(autouse=True)
def setup_test_env(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "dummy_test_key")
    monkeypatch.setenv("SUPABASE_URL", "http://localhost:8000")
    monkeypatch.setenv("SUPABASE_SERVICE_KEY", "dummy_test_key")
    
    # Ensure settings reflect the mocked env vars globally in case they were initialized
    try:
        from app.core.config import settings
        monkeypatch.setattr(settings, "GEMINI_API_KEY", "dummy_test_key")
        monkeypatch.setattr(settings, "SUPABASE_URL", "http://localhost:8000")
        monkeypatch.setattr(settings, "SUPABASE_SERVICE_KEY", "dummy_test_key")
    except ImportError:
        pass

from unittest.mock import patch, MagicMock, AsyncMock

@pytest.mark.asyncio
async def test_translation():
    print("Testing translation...")
    from app.services.llm import get_english_translation
    with patch("app.services.llm.translation_prompt") as mock_prompt, \
         patch("app.services.llm.get_llm") as mock_get_llm, \
         patch("app.services.llm.StrOutputParser") as _mock_parser:
        
        _mock_llm = MagicMock()
        mock_get_llm.return_value = _mock_llm
        mock_chain = MagicMock()
        mock_chain.ainvoke = AsyncMock(return_value="Translated Text")
        mock_chain.__or__.return_value = mock_chain
        mock_prompt.__or__.return_value = mock_chain
        
        translated = await get_english_translation("미덕이란 무엇인가?")
        print("Translation:", translated)
        assert translated == "Translated Text", "Translation output mocked mismatch"
        mock_chain.ainvoke.assert_called_once_with({"query": "미덕이란 무엇인가?"})

def test_streaming():
    print("Testing streaming...")
    from app.services.llm import get_response_stream
    with patch("app.services.llm.get_rag_prompt") as mock_prompt, \
         patch("app.services.llm.get_llm") as mock_get_llm, \
         patch("app.services.llm.StrOutputParser") as _mock_parser:
         
        _mock_llm = MagicMock()
        mock_get_llm.return_value = _mock_llm
        mock_chain = MagicMock()
        mock_chain.stream.return_value = ["안녕하세요", " ", "철학자", "입니다."]
        mock_chain.__or__.return_value = mock_chain
        mock_prompt.return_value.__or__.return_value = mock_chain
        
        stream = get_response_stream(context="Virtue is excellence.", query="What is virtue?")
        results = list(stream)
        assert results == ["안녕하세요", " ", "철학자", "입니다."], "Stream chunks mocked mismatch"
        mock_chain.stream.assert_called_once_with({"context": "Virtue is excellence.", "chat_history": "", "query": "What is virtue?"})

@pytest.mark.asyncio
async def test_streaming_async():
    print("Testing streaming async...")
    from app.services.llm import get_response_stream_async
    with patch("app.services.llm.get_rag_prompt") as mock_prompt, \
         patch("app.services.llm.get_llm") as mock_get_llm, \
         patch("app.services.llm.StrOutputParser") as _mock_parser:
         
        _mock_llm = MagicMock()
        mock_get_llm.return_value = _mock_llm
        mock_chain = MagicMock()
        async def mock_astream(*_args, **_kwargs):
            for chunk in ["안녕하세요", " ", "철학자", "입니다."]:
                yield chunk
        mock_chain.astream = mock_astream
        mock_chain.__or__.return_value = mock_chain
        mock_prompt.return_value.__or__.return_value = mock_chain
        
        stream = get_response_stream_async(context="Virtue is excellence.", query="What is virtue?")
        results = [chunk async for chunk in stream]
        assert results == ["안녕하세요", " ", "철학자", "입니다."], "Async stream chunks mocked mismatch"

# For manual execution
if __name__ == "__main__":
    import pytest
    raise SystemExit(pytest.main([__file__]))
