import sys
from pathlib import Path

# dynamically add backend root dir to path
backend_dir = Path(__file__).resolve().parents[2]
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

import pytest
from typing import Annotated, List, TypedDict

def test_agent_state_definitions():
    """
    LangGraph의 State 구조가 우리가 기획한 필드들을 포함하고 있는지 검증합니다.
    이 테스트는 app.services.graph가 구현되지 않았으므로 실패해야 합니다 (RED).
    """
    try:
        from app.services.graph import AgentState
    except ImportError:
        pytest.fail("app.services.graph module not found (RED phase)")

    # 기획된 상태 필드 목록
    required_keys = [
        "query", 
        "history", 
        "reformulated_query", 
        "documents", 
        "answer", 
        "is_relevant", 
        "retry_count"
    ]
    
    # TypedDict 형식인지 확인 (간접 확인)
    state_annotations = AgentState.__annotations__
    for key in required_keys:
        assert key in state_annotations, f"State must include '{key}' field"

@pytest.mark.asyncio
async def test_workflow_initialization():
    """
    Workflow (StateGraph) 가 정상적으로 컴파일되는지 확인합니다.
    """
    try:
        from app.services.graph import create_graph
    except ImportError:
        pytest.fail("app.services.graph mapping 'create_graph' not found (RED phase)")

    graph = create_graph()
    assert graph is not None
    # graph가 실행 가능한지 여부만 가볍게 체크
    assert hasattr(graph, "ainvoke")
