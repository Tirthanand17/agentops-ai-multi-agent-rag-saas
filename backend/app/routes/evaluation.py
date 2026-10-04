from __future__ import annotations

from fastapi import APIRouter

from ..rag.demo import DEMO_EVAL_CASES
from ..rag.evaluation import retrieval_hit_rate
from .knowledge import rag_service

router = APIRouter(prefix="/evaluation", tags=["evaluation"])


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
