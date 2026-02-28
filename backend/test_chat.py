import asyncio
import os
import sys

# add backend dir to path
sys.path.append(r"c:\Users\ysn65\Desktop\antigravity\philo-rag\backend")

from app.api.routes.chat import generate_chat_events
from fastapi import Request

class DummyRequest:
    async def is_disconnected(self):
        return False

async def test():
    req = DummyRequest()
    generator = generate_chat_events(req, "미덕이란 무엇인가?")
    try:
        async for item in generator:
            print("Item:", item)
    except Exception as e:
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test())
