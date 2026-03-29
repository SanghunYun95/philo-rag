import asyncio
import logging
from typing import Annotated, Dict, List, Literal, TypedDict, Union

from langgraph.graph import END, StateGraph, START
from langchain_core.messages import BaseMessage
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from pydantic import BaseModel, Field

from app.services.llm import get_llm
from app.services.embedding import embedding_service
from app.services.database import get_client

logger = logging.getLogger(__name__)

# Concurrency limit for database RPC calls
_search_semaphore = asyncio.Semaphore(16)

# --- State Definition ---

class AgentState(TypedDict):
    """
    LangGraph 워크플로우의 상태를 정의합니다.
    """
    query: str                       # 사용자 원본 질문 (한국어)
    history: str                     # 대화 이력
    reformulated_query: str          # 검색용으로 재작성된 쿼리 (영어)
    documents: List[Dict]            # 검색된 문서들
    answer: str                      # 최종 생성된 답변
    is_relevant: bool                # 문서의 적합성 여부
    retry_count: int                 # 재시도 횟수

# --- LLM Utils for Nodes ---

class GradeDocuments(BaseModel):
    """검색된 문서의 질문 적합성 여부를 판단하기 위한 스키마"""
    binary_score: str = Field(
        description="Documents are relevant to the question, 'yes' or 'no'"
    )

# --- Nodes Implementation ---

async def rewrite_query(state: AgentState):
    """
    대화 이력을 바탕으로 질문을 검색에 최적화된 영어 쿼리로 재작성합니다.
    """
    logger.info("--- NODE: REWRITE QUERY ---")
    query = state["query"]
    history = state["history"]
    
    prompt = PromptTemplate.from_template(
        """You are an expert at reformulating user queries for better philosophical vector search.
        Given the following chat history and a user query in Korean, rewrite it into a concise, search-optimized English query.
        Focus on core philosophical concepts.
        
        Chat History:
        {history}
        
        User Query:
        {query}
        
        English Search Query:"""
    )
    
    chain = prompt | get_llm() | StrOutputParser()
    reformulated = await chain.ainvoke({"query": query, "history": history or "No history."})
    
    return {"reformulated_query": reformulated.strip()}

async def retrieve(state: AgentState):
    """
    Supabase 백터 스토어에서 문서를 검색합니다.
    """
    logger.info("--- NODE: RETRIEVE ---")
    query = state["reformulated_query"]
    
    # 1. Generate embedding
    query_vector = await embedding_service.agenerate_embedding(query)
    
    # 2. Search in Supabase (RPC match_documents)
    # Note: we use direct RPC call via supabase client
    def _search():
        return get_client().rpc(
            'match_documents', 
            {'query_embedding': query_vector, 'match_count': 4}
        ).execute()
        
    async with _search_semaphore:
        response = await asyncio.to_thread(_search)
    documents = response.data or []
    
    return {"documents": documents}

async def grade_documents(state: AgentState):
    """
    검색된 문서가 질문에 적합한지 가볍게 평가합니다 (Self-Reflection).
    """
    logger.info("--- NODE: GRADE DOCUMENTS ---")
    query = state["reformulated_query"]
    docs = state["documents"]
    
    if not docs:
        return {"is_relevant": False, "retry_count": state.get("retry_count", 0) + 1}
    
    # Safe access to document content; Filter out empty content
    context_text = "\n\n".join([d.get("content", "") for d in docs if d.get("content")])
    if not context_text.strip():
        return {"is_relevant": False, "retry_count": state.get("retry_count", 0) + 1}
    
    prompt = PromptTemplate.from_template(
        """You are a grader assessing relevance of a retrieved document to a user question.
        If the document contains keywords or semantic meaning related to the user question, grade it as relevant. 
        Give a binary score 'yes' or 'no' score to indicate whether the document is relevant to the question.

        Retrieved Documents:
        {context}

        User Question:
        {query}
        
        Output format: {{"binary_score": "yes" | "no"}}"""
    )
    
    # Use structured LLM via helper that applies it to fallbacks
    chain = prompt | get_llm(structured_schema=GradeDocuments)
    scored_result = await chain.ainvoke({"query": query, "context": context_text})
    
    is_relevant = scored_result.binary_score.lower() == "yes"
    logger.info(f"--- GRADING RESULT: {scored_result.binary_score} ---")
    
    new_retry_count = state.get("retry_count", 0)
    if not is_relevant:
        new_retry_count += 1
        
    return {"is_relevant": is_relevant, "retry_count": new_retry_count}

async def generate(state: AgentState):
    """
    최종 답변을 생성합니다. (실제 스트리밍은 API 라우트에서 별도로 처리될 수 있음)
    """
    logger.info("--- NODE: GENERATE ---")
    from app.services.llm import get_rag_prompt
    
    query = state["query"]
    history = state["history"]
    docs = state.get("documents", [])
    context = "\n\n".join([d.get("content", "") for d in docs if d.get("content")])
    
    prompt = get_rag_prompt()
    chain = prompt | get_llm().with_config({"tags": ["final_generation"]}) | StrOutputParser()
    
    # Generate batch response (streaming case is handled differently via astream_events)
    answer = await chain.ainvoke({"context": context, "chat_history": history, "query": query})
    
    return {"answer": answer}

# --- Router Logic ---

def decide_to_generate(state: AgentState):
    """
    RELEVANCE 결과에 따라 다음 노드를 결정합니다.
    """
    if state["is_relevant"] or state["retry_count"] >= 2:
        return "generate"
    else:
        return "rewrite_query"

# --- Graph Construction ---

def create_graph():
    workflow = StateGraph(AgentState)
    
    # Add Nodes
    workflow.add_node("rewrite_query", rewrite_query)
    workflow.add_node("retrieve", retrieve)
    workflow.add_node("grade_documents", grade_documents)
    workflow.add_node("generate", generate)
    
    # Add Edges
    workflow.add_edge(START, "rewrite_query")
    workflow.add_edge("rewrite_query", "retrieve")
    workflow.add_edge("retrieve", "grade_documents")
    
    # Conditional Edge (Self-Reflection Loop)
    workflow.add_conditional_edges(
        "grade_documents",
        decide_to_generate,
        {
            "generate": "generate",
            "rewrite_query": "rewrite_query"
        }
    )
    
    workflow.add_edge("generate", END)
    
    return workflow.compile()
