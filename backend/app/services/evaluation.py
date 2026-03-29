import logging
import asyncio
from typing import List

try:
    from ragas import evaluate
    from ragas.metrics import Faithfulness, AnswerRelevancy
    from datasets import Dataset
except ImportError:
    evaluate = None
    Faithfulness = None
    AnswerRelevancy = None
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
        
        def _run_evaluate_and_log():
            from app.services.llm import get_llm
            from app.services.embedding import embedding_service
            
            # 1. Evaluate using Ragas
            llm = get_llm(new_instance=True)
            embeddings = embedding_service.embeddings
            
            result = evaluate(
                dataset=dataset,
                metrics=[Faithfulness(), AnswerRelevancy()],
                llm=llm,
                embeddings=embeddings
            )
            logger.info(f"Ragas evaluation completed: {result}")
            
            # Extract scores securely
            try:
                faithfulness_score = result["faithfulness"]
                answer_relevance_score = result["answer_relevancy"]
            except (TypeError, KeyError):
                faithfulness_score = result.scores.get("faithfulness", 0.0)
                answer_relevance_score = result.scores.get("answer_relevancy", 0.0)
                
            if isinstance(faithfulness_score, list) and len(faithfulness_score) > 0:
                faithfulness_score = faithfulness_score[0]
            if isinstance(answer_relevance_score, list) and len(answer_relevance_score) > 0:
                answer_relevance_score = answer_relevance_score[0]
                
            import math
            def safe_float(v):
                try:
                    val = float(v)
                    return val if not math.isnan(val) else 0.0
                except (TypeError, ValueError):
                    return 0.0
            
            f_score = safe_float(faithfulness_score)
            a_score = safe_float(answer_relevance_score)
            
            # 2. Insert into DB (within the same thread to keep everything out of event loop)
            db = get_client()
            log_data = {
                "query": query,
                "reformulated_query": reformulated_query,
                "answer": answer,
                "context_relevance": float(context_relevance),
                "faithfulness": f_score,
                "answer_relevance": a_score,
                "metadata": {
                    "evaluated_by": "ragas",
                    "length": len(answer),
                    "retrieved_contexts": contexts
                }
            }
            db.table("eval_logs").insert(log_data).execute()
            logger.info("Successfully inserted into Supabase.")
            return f_score, a_score
            
        await asyncio.to_thread(_run_evaluate_and_log)
        
    except Exception as e:
        logger.exception("Failed during evaluate_and_log background task.")

