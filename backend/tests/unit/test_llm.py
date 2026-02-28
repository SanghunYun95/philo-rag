import asyncio
import os
import sys
import pytest
from pathlib import Path

# dynamically add backend dir to path
backend_dir = Path(__file__).resolve().parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from app.services.llm import get_english_translation, get_response_stream
from app.core.config import settings

@pytest.mark.skipif(not settings.GEMINI_API_KEY, reason="GEMINI_API_KEY is not configured")
def test_translation():
    print("Testing translation...")
    try:
        translated = get_english_translation("미덕이란 무엇인가?")
        print("Translation:", translated)
        assert translated.strip() != "", "Translation must not be empty"
    except Exception as e:
        raise AssertionError(f"Translation error: {str(e)}")

@pytest.mark.skipif(not settings.GEMINI_API_KEY, reason="GEMINI_API_KEY is not configured")
def test_streaming():
    print("Testing streaming...")
    try:
        stream = get_response_stream(context="Virtue is excellence.", query="What is virtue?")
        chunks_received = 0
        for chunk in stream:
            print(chunk, end="", flush=True)
            chunks_received += 1
        print("\nStream finished")
        assert chunks_received > 0, "No chunks received from streaming API"
    except Exception as e:
        raise AssertionError(f"Stream error: {str(e)}")

# For manual execution
async def run_manual_test():
    test_translation()
    test_streaming()

if __name__ == "__main__":
    asyncio.run(run_manual_test())
