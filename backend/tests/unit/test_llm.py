import asyncio
import os
import sys
import pytest
from pathlib import Path

# dynamically add backend root dir to path
backend_dir = Path(__file__).resolve().parents[2]
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from unittest.mock import patch, MagicMock
from app.services.llm import get_english_translation, get_response_stream

def test_translation():
    print("Testing translation...")
    try:
        with patch("app.services.llm.translation_prompt") as mock_prompt, \
             patch("app.services.llm.llm") as mock_llm, \
             patch("app.services.llm.StrOutputParser") as mock_parser:
            
            mock_chain = MagicMock()
            mock_chain.invoke.return_value = "Translated Text"
            mock_prompt.__or__.return_value.__or__.return_value = mock_chain
            
            translated = get_english_translation("미덕이란 무엇인가?")
            print("Translation:", translated)
            assert translated == "Translated Text", "Translation output mocked mismatch"
    except Exception as e:
        raise AssertionError(f"Translation error: {e}") from e

def test_streaming():
    print("Testing streaming...")
    try:
        with patch("app.services.llm.get_rag_prompt") as mock_prompt, \
             patch("app.services.llm.llm") as mock_llm, \
             patch("app.services.llm.StrOutputParser") as mock_parser:
             
            mock_chain = MagicMock()
            mock_chain.stream.return_value = (chunk for chunk in ["안녕하세요", " ", "철학자", "입니다."])
            mock_prompt.return_value.__or__.return_value.__or__.return_value = mock_chain
            
            stream = get_response_stream(context="Virtue is excellence.", query="What is virtue?")
            results = list(stream)
            assert results == ["안녕하세요", " ", "철학자", "입니다."], "Stream chunks mocked mismatch"
    except Exception as e:
        raise AssertionError(f"Stream error: {e}") from e

# For manual execution
if __name__ == "__main__":
    test_translation()
    test_streaming()
