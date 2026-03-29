import sys
from pathlib import Path

# dynamically add backend root dir to path
backend_dir = Path(__file__).resolve().parents[2]
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

import pytest
from unittest.mock import patch, MagicMock, AsyncMock

@pytest.mark.asyncio
async def test_evaluate_and_log():
    """
    evaluate_and_log 함수가 정상적으로 ragas 채점을 수행하고 DB에 로그를 저장하는지 검증합니다.
    (RED Phase - 구현체 없음)
    """
    try:
        from app.services.evaluation import evaluate_and_log
    except ImportError:
        pytest.fail("app.services.evaluation module not found (RED phase)")

    # 모킹: ragas의 evaluate 함수와 supabase insert
    with patch("app.services.evaluation.evaluate") as mock_eval, \
         patch("app.services.evaluation.get_client") as mock_get_client:
        
        # mock evaluate result
        mock_eval.return_value = {
            "faithfulness": 0.85,
            "answer_relevancy": 0.90
        }
        
        # mock supabase insert
        mock_db = MagicMock()
        mock_get_client.return_value = mock_db
        mock_table = MagicMock()
        mock_db.table.return_value = mock_table
        mock_insert = MagicMock()
        mock_table.insert.return_value = mock_insert
        mock_insert.execute = MagicMock()

        # Run evaluation background task
        await evaluate_and_log(
            query="인간의 본성은 선한가?",
            reformulated_query="Is human nature inherently good?",
            contexts=["맹자에 따르면 인간의 본성은 선하다(성선설)."],
            answer="맹자는 인간의 본성이 선하다고 주장했습니다.",
            context_relevance=1.0
        )
        
        # Verify evaluate was called
        mock_eval.assert_called_once()
        
        # Verify DB insert was called with Correct Data
        mock_db.table.assert_called_once_with("eval_logs")
        insert_args = mock_table.insert.call_args[0][0]
        
        assert insert_args["query"] == "인간의 본성은 선한가?"
        assert insert_args["faithfulness"] == 0.85
        assert insert_args["answer_relevance"] == 0.90
