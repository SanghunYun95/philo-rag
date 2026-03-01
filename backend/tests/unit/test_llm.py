
import sys
import pytest
from pathlib import Path

# dynamically add backend root dir to path
backend_dir = Path(__file__).resolve().parents[2]
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

import os
os.environ["GEMINI_API_KEY"] = "dummy_test_key"
os.environ["SUPABASE_URL"] = "http://localhost:8000"
os.environ["SUPABASE_SERVICE_KEY"] = "dummy_test_key"

from unittest.mock import patch, MagicMock
from app.services.llm import get_english_translation, get_response_stream, get_response_stream_async

def test_translation():
    print("Testing translation...")
    with patch("app.services.llm.translation_prompt") as mock_prompt, \
         patch("app.services.llm.llm") as _mock_llm, \
         patch("app.services.llm.StrOutputParser") as _mock_parser:
        
        mock_chain = MagicMock()
        mock_chain.invoke.return_value = "Translated Text"
        mock_chain.__or__.return_value = mock_chain
        mock_prompt.__or__.return_value = mock_chain
        
        translated = get_english_translation("미덕이란 무엇인가?")
        print("Translation:", translated)
        assert translated == "Translated Text", "Translation output mocked mismatch"

def test_streaming():
    print("Testing streaming...")
    with patch("app.services.llm.get_rag_prompt") as mock_prompt, \
         patch("app.services.llm.llm") as _mock_llm, \
         patch("app.services.llm.StrOutputParser") as _mock_parser:
         
        mock_chain = MagicMock()
        mock_chain.stream.return_value = ["안녕하세요", " ", "철학자", "입니다."]
        mock_chain.__or__.return_value = mock_chain
        mock_prompt.return_value.__or__.return_value = mock_chain
        
        stream = get_response_stream(context="Virtue is excellence.", query="What is virtue?")
        results = list(stream)
        assert results == ["안녕하세요", " ", "철학자", "입니다."], "Stream chunks mocked mismatch"

@pytest.mark.asyncio
async def test_streaming_async():
    print("Testing streaming async...")
    with patch("app.services.llm.get_rag_prompt") as mock_prompt, \
         patch("app.services.llm.llm") as _mock_llm, \
         patch("app.services.llm.StrOutputParser") as _mock_parser:
         
        mock_chain = MagicMock()
        async def mock_astream(*args, **kwargs):
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
    import asyncio
    test_translation()
    test_streaming()
    asyncio.run(test_streaming_async())
