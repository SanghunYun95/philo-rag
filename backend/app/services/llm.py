import google.generativeai as genai
from app.core.config import settings
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser

# Configure Gemini API natively (optional, if native SDK features are needed)
genai.configure(api_key=settings.GEMINI_API_KEY)

# Configure LangChain model
# We use gemini-2.5-flash for faster and highly capable inference
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash", 
    google_api_key=settings.GEMINI_API_KEY or "dummy_key_for_testing",
    temperature=0.7,
    max_retries=0
)

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
    chain = translation_prompt | llm | StrOutputParser()
    return chain.invoke({"query": korean_query})

def get_rag_prompt() -> PromptTemplate:
    """
    Returns the core RAG prompt template taking English context and the translated query,
    requesting the output in Korean.
    """
    template = """
    You are 'PhiloRAG', a philosophical chatbot providing wisdom and comfort based on Eastern and Western philosophies.
    Use the following English philosophical context to answer the user's question.
    Your final answer must be in Korean. 
    
    Context:
    {context}
    
    User Query (English translation):
    {query}
    
    Philosophical Prescription (in Korean):
    """
    return PromptTemplate.from_template(template)

def get_response_stream(context: str, query: str):
    """
    Returns a stream of strings from the LLM.
    """
    prompt = get_rag_prompt()
    chain = prompt | llm | StrOutputParser()
    return chain.stream({"context": context, "query": query})
