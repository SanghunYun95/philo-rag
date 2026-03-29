import logging
import asyncio
from typing import List

try:
    from ragas import evaluate
    from ragas.metrics.collections import faithfulness, answer_relevancy
    from datasets import Dataset
except ImportError:
    evaluate = None
    faithfulness = None
    answer_relevancy = None
    Dataset = None

from app.services.database import get_client

logger = logging.getLogger(__name__)

async def evaluate_and_log(
    query: str,
    reformulated_query: str,
    contexts: List[str],
    answer: str,
    context_relevance: float = 0.0
):
    """
    RAGAS를 통해 모델의 답변 품질을 비동기로 평가하고 Supabase DB에 로그를 남깁니다.
    """
    if evaluate is None:
        logger.warning("RAGAS dependencies not found. Skipping evaluation.")
        return
        
    logger.info("Starting async evaluate_and_log", extra={"query_len": len(query)})
    
    try:
        data = {
            "question": [query],
            "contexts": [contexts],
            "answer": [answer]
        }
        dataset = Dataset.from_dict(data)
        
        def _run_evaluate():
            from app.services.llm import get_llm
            from app.services.embedding import embedding_service
            
            llm = get_llm(new_instance=True)
            embeddings = embedding_service.embeddings
            
            # Using new collection-style metrics from ragas v0.4+
            return evaluate(
                dataset=dataset,
                metrics=[faithfulness(), answer_relevancy()],
                llm=llm,
                embeddings=embeddings
            )
            
        result = await asyncio.to_thread(_run_evaluate)
        logger.info(f"Ragas evaluation result: {result}")
        
        # Result object usually behaves like a dict or has .scores
        try:
            faithfulness_score = result["faithfulness"]
            answer_relevance_score = result["answer_relevancy"]
        except (TypeError, KeyError):
            # Fallback if result is a raw Results object or something else
            faithfulness_score = result.scores.get("faithfulness", 0.0)
            answer_relevance_score = result.scores.get("answer_relevancy", 0.0)
            
        # If result is a list (single row evaluation), take the first element
        if isinstance(faithfulness_score, list) and len(faithfulness_score) > 0:
            faithfulness_score = faithfulness_score[0]
        if isinstance(answer_relevance_score, list) and len(answer_relevance_score) > 0:
            answer_relevance_score = answer_relevance_score[0]
            
        # Final cleanup for NaN/None values which Ragas sometimes returns
        import math
        def safe_float(v):
            try:
                val = float(v)
                return val if not math.isnan(val) else 0.0
            except (TypeError, ValueError):
                return 0.0
        
        faithfulness_score = safe_float(faithfulness_score)
        answer_relevance_score = safe_float(answer_relevance_score)
        
        # Insert into DB
        db = get_client()
        log_data = {
            "query": query,
            "reformulated_query": reformulated_query,
            "answer": answer,
            "context_relevance": float(context_relevance),
            "faithfulness": faithfulness_score,
            "answer_relevance": answer_relevance_score,
            "metadata": {
                "evaluated_by": "ragas",
                "length": len(answer),
                "retrieved_contexts": contexts
            }
        }
        
        logger.info(
            "Inserting into Supabase eval_logs",
            extra={
                "query_len": len(query),
                "ans_len": len(answer),
                "ctx_count": len(contexts)
            }
        )
        db.table("eval_logs").insert(log_data).execute()
        logger.info("Successfully inserted into Supabase.")
        
    except Exception as e:
        logger.exception("Failed during evaluate_and_log background task.")
