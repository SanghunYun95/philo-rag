import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path=env_path)

import sys

def main() -> int:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("No API key found!")
        return 1

    client = OpenAI(api_key=api_key)
    print("Available Models:")
    try:
        models = client.models.list()
        for m in models:
            print(m.id)
    except Exception as e:
        print(f"Error listing models: {e}")
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())
