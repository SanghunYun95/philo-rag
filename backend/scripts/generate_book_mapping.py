import os
import re
import json
import asyncio
import sys
from pathlib import Path
from dotenv import load_dotenv
import urllib.request
import urllib.parse
import urllib.error
import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted

backend_dir = Path(__file__).resolve().parents[1]
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

env_path = backend_dir.parent / ".env"
print(f"Loading .env from {env_path}, exists: {env_path.exists()}")
load_dotenv(dotenv_path=env_path)

# Extract ALL GEMINI_API_KEYs from .env file
api_keys = []
if env_path.exists():
    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            m = re.match(r'^\s*GEMINI_API_KEY\s*=\s*(.+?)\s*(?:#.*)?$', line)
            if not m:
                continue
            key = m.group(1).strip().strip('"').strip("'")
            if key and key not in api_keys:
                api_keys.append(key)
else:
    # Fallback to os.environ if .env missing
    k = os.getenv("GEMINI_API_KEY")
    if k:
        api_keys.append(k)

# The user explicitly asked to start testing from new keys (lines 8~14), and then go back to line 2.
if len(api_keys) >= 4:
    api_keys = api_keys[3:] + api_keys[:3]

current_key_idx = 0

DATA_DIR = backend_dir / "data"
MAPPING_FILE = backend_dir / "data" / "books_mapping.json"
ALADIN_API_KEY = os.getenv("ALADIN_API_KEY")

prompt_template = """You are given an English file name representing a philosophical book and its author.
Your task is to provide the standard, most well-known Korean translation title for this book, and the author's name in Korean.
Return ONLY JSON format exactly like this, without any markdown formatting or explanations:
{{"title": "한국어 번역본 책 제목", "author": "한국어 저자 이름"}}

File name: {file_name}
"""

async def kyobo_fallback(title: str, author: str) -> dict:
    clean_title = title.replace(".txt", "").replace("_", " ")
    query = f"{clean_title}".strip()
    encoded_query = urllib.parse.quote(query)
    url = f"https://search.kyobobook.co.kr/search?keyword={encoded_query}"
    
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    
    loop = asyncio.get_running_loop()
    def fetch():
        try:
            with urllib.request.urlopen(req, timeout=10) as response:
                return response.read().decode('utf-8')
        except urllib.error.URLError as e:
            print(f"Kyobo network error: {e}")
            return None
        except Exception as e:
            print(f"Kyobo undefined error: {e}")
            raise
            
    html = await loop.run_in_executor(None, fetch)
    if not html:
        return {"kr_title": clean_title, "kr_author": author}
    
    match = re.search(r'<span class="prod_name">(.*?)</span>', html)
    if match:
        kr_title = match.group(1).strip()
        kr_title = re.sub(r'<[^>]+>', '', kr_title) # Remove internal tags
        return {"kr_title": kr_title, "kr_author": author}
    
    return {"kr_title": clean_title, "kr_author": author}

async def translate_book_info(file_name: str) -> dict:
    global current_key_idx
    
    while current_key_idx < len(api_keys):
        key = api_keys[current_key_idx]
        genai.configure(api_key=key)
        # Using gemini-2.5-flash-lite as it has a higher free tier
        model = genai.GenerativeModel("gemini-2.5-flash-lite")
        
        try:
            response = await model.generate_content_async(
                prompt_template.format(file_name=file_name),
                generation_config=genai.types.GenerationConfig(temperature=0.7)
            )
            result_text = response.text
            clean_text = result_text.replace("```json", "").replace("```", "").strip()
            data = json.loads(clean_text)
            return {"kr_title": data["title"], "kr_author": data["author"]}
            
        except ResourceExhausted:
            print(f"API Key {current_key_idx} exhausted. Switching to next key...")
            current_key_idx += 1
        except Exception as e:
            error_str = str(e).lower()
            if "429" in error_str or "quota" in error_str or "exhausted" in error_str or "toomanyrequests" in error_str:
                print(f"API Key {current_key_idx} exhausted. Switching to next key...")
                current_key_idx += 1
            else:
                print(f"Failed to parse LLM translation for {file_name}: {e}")
                break
                
    # If all keys exhausted or other error, fallback
    print(f"LLM Failed for {file_name}, falling back to Kyobo Search...")
    return await kyobo_fallback(file_name, "")

async def search_aladin(title: str, author: str) -> dict:
    if not ALADIN_API_KEY:
        print(f"Warning: ALADIN_API_KEY is not set. Skipping search for {title}")
        return {}
        
    query = f"{title} {author}".strip()
    url = f"http://www.aladin.co.kr/ttb/api/ItemSearch.aspx?ttbkey={ALADIN_API_KEY}&Query={urllib.parse.quote(query)}&QueryType=Keyword&MaxResults=1&start=1&SearchTarget=Book&output=js&Version=20131101"
    
    try:
        loop = asyncio.get_running_loop()
        def fetch():
            with urllib.request.urlopen(url, timeout=10) as response:
                return response.read().decode('utf-8')
        
        response_text = await loop.run_in_executor(None, fetch)
        data = json.loads(response_text)
        
        items = data.get("item", [])
        if items:
            item = items[0]
            return {
                "title": item.get("title", ""),
                "link": item.get("link", ""),
                "thumbnail": item.get("cover", ""),
                "author": item.get("author", ""),
                "isbn": item.get("isbn13", "")
            }
    except Exception as e:
        print(f"Aladin API Error for {query}: {e}")
        
    return {}

async def process_file(file_path: Path):
    file_name = file_path.stem
    print(f"Processing: {file_name}")
    
    translated = await translate_book_info(file_name)
    kr_title = translated["kr_title"]
    kr_author = translated["kr_author"]
    
    aladin_data = await search_aladin(kr_title, kr_author)
    
    return {
        "original_file": file_path.name,
        "translated_title": kr_title,
        "translated_author": kr_author,
        "aladin_data": aladin_data
    }

async def main():
    if not DATA_DIR.exists():
        print(f"Data directory not found at {DATA_DIR}")
        return
        
    txt_files = list(DATA_DIR.glob("*.txt"))
    print(f"Found {len(txt_files)} text files.")
    
    mapping = []
    if MAPPING_FILE.exists():
        with open(MAPPING_FILE, "r", encoding="utf-8") as f:
            try:
                mapping = json.load(f)
            except json.JSONDecodeError:
                mapping = []
            
    existing_files = {item["original_file"] for item in mapping}
    files_to_process = [f for f in txt_files if f.name not in existing_files]
    
    print(f"Skipping {len(existing_files)} already processed files. Processing {len(files_to_process)} new files.")
    print(f"Loaded {len(api_keys)} API keys for rotation.")
    
    for i, f in enumerate(files_to_process):
        try:
            result = await process_file(f)
            mapping.append(result)
            
            tmp_file = MAPPING_FILE.with_suffix(".json.tmp")
            with open(tmp_file, "w", encoding="utf-8") as out_f:
                json.dump(mapping, out_f, ensure_ascii=False, indent=4)
            tmp_file.replace(MAPPING_FILE)
                
            print(f"Processed {i + 1}/{len(files_to_process)}, sleeping for 4s...")
            await asyncio.sleep(4.1)
        except Exception as e:
            print(f"Error processing {f.name}: {e}")
            await asyncio.sleep(4.1)
        
    print(f"Finished mapping. Total mapped: {len(mapping)}")

if __name__ == "__main__":
    asyncio.run(main())
