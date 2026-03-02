import threading
import google.generativeai as genai
from app.core.config import settings
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser

# Models will be instantiated lazily or during function call
_llm = None
_llm_lock = threading.Lock()

def get_llm():
    global _llm
    if not settings.GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY must be configured")
        
    if _llm is None:
        with _llm_lock:
            if _llm is None:  # Double-checked locking
                # Configure Gemini API natively (optional, if native SDK features are needed)
                genai.configure(api_key=settings.GEMINI_API_KEY)
                
                # Configure LangChain model
                # TODO: model gemini-2.5-flash will be deprecated by June 17, 2026. Plan migration to gemini-3-flash.
                _llm = ChatGoogleGenerativeAI(
                    model="gemini-3-flash", 
                    google_api_key=settings.GEMINI_API_KEY,
                    temperature=0.7,
                    max_retries=2
                )
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
