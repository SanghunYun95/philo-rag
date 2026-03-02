import os
import re
import threading
from pathlib import Path
import google.generativeai as genai
from app.core.config import settings
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser

# Models will be instantiated lazily or during function call
_llm = None
_llm_lock = threading.Lock()

def get_all_gemini_keys() -> list[str]:
    """Reads all active and commented GEMINI_API_KEYs from the root .env file."""
    keys = []
    env_path = Path(__file__).resolve().parents[3] / ".env"
    
    if env_path.exists():
        with open(env_path, "r", encoding="utf-8") as f:
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
                if key and key not in keys:
                    keys.append(key)
                    
    # Ensure the one from environment variables/settings is also included
    if getattr(settings, "GEMINI_API_KEY", None) and settings.GEMINI_API_KEY not in keys:
        keys.insert(0, settings.GEMINI_API_KEY)
        
    return keys

def get_llm():
    global _llm
    if _llm is None:
        with _llm_lock:
            if _llm is None:  # Double-checked locking
                keys = get_all_gemini_keys()
                
                if not keys:
                    raise RuntimeError("No GEMINI_API_KEY found in .env or environment")
                
                # Configure Gemini API natively with the first key
                genai.configure(api_key=keys[0])
                
                print(f"Loaded {len(keys)} Gemini API keys for rotation/fallbacks.")
                
                # Create the primary model
                primary_llm = ChatGoogleGenerativeAI(
                    model="gemini-2.5-flash-lite", 
                    google_api_key=keys[0],
                    temperature=0.7,
                    max_retries=1
                )
                
                if len(keys) > 1:
                    # Create fallback models with the other keys
                    fallback_llms = [
                        ChatGoogleGenerativeAI(
                            model="gemini-2.5-flash-lite", 
                            google_api_key=k,
                            temperature=0.7,
                            max_retries=1
                        )
                        for k in keys[1:]
                    ]
                    # LangChain will automatically retry with the next model if one throws an error (e.g. rate limit / quota)
                    _llm = primary_llm.with_fallbacks(fallback_llms)
                else:
                    _llm = primary_llm
                    
    return _llm


translation_prompt = PromptTemplate.from_template(
    """Translate the following user query from Korean to English.
    Only output the translated text without any other explanations.
    
    Query: {query}
    Translation: """
)

def get_english_translation(korean_query: str) -> str:
    """
    Translates a Korean query to English using Gemini via LangChain.
    """
    chain = translation_prompt | get_llm() | StrOutputParser()
    return chain.invoke({"query": korean_query})

def get_rag_prompt() -> PromptTemplate:
    """
    Returns the core RAG prompt template taking English context, history, and the translated query,
    requesting the output in Korean.
    """
    template = """
    You are 'PhiloRAG', a philosophical chatbot providing wisdom and comfort based on Eastern and Western philosophies.
    Use the following English philosophical context and the chat history to answer the user's question.
    Your final answer must be in Korean. 
    
    Context:
    {context}
    
    Recent Chat History:
    {chat_history}
    
    User Query (English translation):
    {query}
    
    Philosophical Prescription (in Korean):
    """
    return PromptTemplate.from_template(template)

def get_response_stream(context: str, query: str, history: str = ""):
    """
    Returns a stream of strings from the LLM.
    """
    prompt = get_rag_prompt()
    chain = prompt | get_llm() | StrOutputParser()
    return chain.stream({"context": context, "chat_history": history, "query": query})

async def get_response_stream_async(context: str, query: str, history: str = ""):
    """
    Returns an async stream of strings from the LLM.
    """
    prompt = get_rag_prompt()
    chain = prompt | get_llm() | StrOutputParser()
    async for chunk in chain.astream({"context": context, "chat_history": history, "query": query}):
        yield chunk
