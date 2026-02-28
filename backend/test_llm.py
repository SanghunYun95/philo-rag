import asyncio
import os
import sys

# add backend dir to path
sys.path.append(r"c:\Users\ysn65\Desktop\antigravity\philo-rag\backend")

from app.services.llm import get_english_translation, get_response_stream

async def test():
    print("Testing translation...")
    try:
        translated = get_english_translation("미덕이란 무엇인가?")
        print("Translation:", translated)
    except Exception as e:
        print("Translation error:", e)
        return

    print("Testing streaming...")
    try:
        stream = get_response_stream(context="Virtue is excellence.", query="What is virtue?")
        for chunk in stream:
            print(chunk, end="", flush=True)
        print("\nStream finished")
    except Exception as e:
        print("Stream error:", e)

if __name__ == "__main__":
    asyncio.run(test())
