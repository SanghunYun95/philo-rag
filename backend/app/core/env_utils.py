import os
import re
from pathlib import Path

def parse_gemini_api_keys(env_path: Path) -> list[str]:
    """
    Reads active GEMINI_API_KEY assignments from the given .env file.
    Only extracts active assignments and strips inline comments and quotes.
    Also falls back to os.environ if no keys are found in the file.
    """
    api_keys = []
    
    if env_path.exists():
        with open(env_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Find all variations of GEMINI_API_KEY assignments
            matches = re.findall(
                r'^\s*GEMINI_API_KEY\s*=\s*(.+?)\s*(?:#.*)?$',
                content,
                flags=re.MULTILINE,
            )
            for m in matches:
                # Remove inline comments and strip quotes
                m = re.split(r'\s+#', m, 1)[0]
                key = m.strip().strip('"').strip("'")
                if key and key not in api_keys:
                    api_keys.append(key)
                    
    # Fallback to os.environ when parsing produced no key or file doesn't exist
    if not api_keys:
        k = os.getenv("GEMINI_API_KEY")
        if k and k not in api_keys:
            api_keys.append(k)
            
    return api_keys
