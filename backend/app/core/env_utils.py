import os
import re
from pathlib import Path

def parse_openai_api_keys(env_path: Path) -> list[str]:
    """
    Reads active OPENAI_API_KEY assignments from the given .env file.
    Extracts active assignments and strips inline comments and quotes.
    Also merges OPENAI_API_KEYS (comma-separated) and OPENAI_API_KEY
    from os.environ with de-duplication, preserving first-seen order.
    """
    def _normalize_key(value: str) -> str:
        return value.strip().strip('"').strip("'") if value else ""
    api_keys = []
    
    if env_path.is_file():
        with open(env_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Find all variations of OPENAI_API_KEY assignments
            matches = re.findall(
                r'^\s*OPENAI_API_KEY\s*=\s*(.+?)\s*(?:#.*)?$',
                content,
                flags=re.MULTILINE,
            )
            for m in matches:
                # Remove inline comments and strip quotes
                m = re.split(r'\s+#', m, 1)[0]
                key = _normalize_key(m)
                if key and key not in api_keys:
                    api_keys.append(key)
                    
    # Also check OPENAI_API_KEYS (comma-separated list) from environment variables
    # This is highly useful for deployment environments like Render
    env_keys_str = os.getenv("OPENAI_API_KEYS")
    if env_keys_str:
        for k in env_keys_str.split(','):
            key = _normalize_key(k)
            if key and key not in api_keys:
                api_keys.append(key)
                
    # Also merge single OPENAI_API_KEY from environment (if present)
    k = os.getenv("OPENAI_API_KEY")
    if k:
        key = _normalize_key(k)
        if key and key not in api_keys:
            api_keys.append(key)
            
    return api_keys
