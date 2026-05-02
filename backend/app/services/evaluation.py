import logging
import asyncio
import threading
from typing import List

# Concurrency limit for heavy RAGAS evaluations to prevent thread pool exhaustion and OOM
# RAGAS evaluation can take 20-60s per call; limiting to 1 concurrent run on small Cloud Run instances.
_eval_semaphore = asyncio.Semaphore(1)

# Global placeholders for lazy-loaded RAGAS dependencies (initialized inside the thread)
_ragas_initialized = False
_ragas_lock = threading.Lock()
evaluate = None
Faithfulness = None
AnswerRelevancy = None
Dataset = None

from app.services.database import get_client

logger = logging.getLogger(__name__)

def _init_ragas():
    global evaluate, Faithfulness, AnswerRelevancy, Dataset, _ragas_initialized
    if not _ragas_initialized:
        with _ragas_lock:
            if not _ragas_initialized:
                try:
                    logger.info("Loading RAGAS and dependencies...")
                    from ragas import evaluate as _eval
                    from ragas.metrics import Faithfulness as _Faith, AnswerRelevancy as _ARel
                    from datasets import Dataset as _DS
                    evaluate = _eval
                    Faithfulness = _Faith
                    AnswerRelevancy = _ARel
                    Dataset = _DS
                    _ragas_initialized = True
                    logger.info("RAGAS loaded successfully.")
                except ImportError:
                    logger.warning("RAGAS dependencies not found.")
                    return False
    return True

async def warmup_evaluation():
    """Trigger lazy loading of RAGAS in a background thread."""
    await asyncio.to_thread(_init_ragas)

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
    logger.info("Starting evaluate_and_log", extra={"query_len": len(query)})
    
    try:
        # Limit concurrency using semaphore
        async with _eval_semaphore:
            logger.info("Acquired evaluation semaphore. Running in thread...")
            
            def _run_evaluate_and_log():
                _init_ragas()
                if evaluate is None:
                    return None

                from app.services.llm import get_llm
                from app.services.embedding import embedding_service
                
                # 1. Prepare Dataset
                data = {
                    "question": [query],
                    "contexts": [contexts],
                    "answer": [answer]
                }
                dataset = Dataset.from_dict(data)
                
                # 2. Evaluate using Ragas
                logger.info("Evaluating with RAGAS (this may take time)...")
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
                
                # 3. Insert into DB (within the same thread to keep everything out of event loop)
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

