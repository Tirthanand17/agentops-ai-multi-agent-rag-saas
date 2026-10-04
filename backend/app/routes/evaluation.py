from __future__ import annotations

from fastapi import APIRouter

from ..agent_state import agent_runtime
from ..agents.evaluation import AgentEvalCase, tool_selection_accuracy
from ..rag.demo import DEMO_EVAL_CASES
from ..rag.evaluation import retrieval_hit_rate
from ..state import rag_service

router = APIRouter(prefix="/evaluation", tags=["evaluation"])

AGENT_EVAL_CASES = [
    AgentEvalCase(
        request="What is the refund window?",
        expected_tools=("knowledge_search",),
    ),
    AgentEvalCase(
        request="Check order 1042.",
        expected_tools=("order_lookup",),
    ),
    AgentEvalCase(
        request="Escalate Acme and create a support ticket.",
        expected_tools=("knowledge_search", "create_ticket"),
    ),
]


@router.get("/rag")
def evaluate_rag() -> dict[str, object]:
    hit_rate = retrieval_hit_rate(
        rag_service,
        DEMO_EVAL_CASES,
        top_k=2,
    )
    return {
        "dataset": "demo-retail-v1",
        "cases": len(DEMO_EVAL_CASES),
        "retrieval_hit_rate_at_2": round(hit_rate, 4),
        "passed": hit_rate == 1.0,
    }


@router.get("/agents")
def evaluate_agents() -> dict[str, object]:
    accuracy = tool_selection_accuracy(
        agent_runtime,
        "demo-retail",
        AGENT_EVAL_CASES,
    )
    return {
        "dataset": "demo-agent-routing-v1",
        "cases": len(AGENT_EVAL_CASES),
        "tool_selection_accuracy": round(accuracy, 4),
        "passed": accuracy == 1.0,
    }
