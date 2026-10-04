from __future__ import annotations

from dataclasses import dataclass

from .service import RAGService


@dataclass(frozen=True)
class RetrievalCase:
    workspace_id: str
    query: str
    expected_source_id: str


def retrieval_hit_rate(
    service: RAGService,
    cases: list[RetrievalCase],
    top_k: int = 3,
) -> float:
    if not cases:
        return 0.0

    hits = 0
    for case in cases:
        results = service.search(
            workspace_id=case.workspace_id,
            query=case.query,
            top_k=top_k,
        )
        source_ids = {hit.chunk.source_id for hit in results}
        hits += int(case.expected_source_id in source_ids)

    return hits / len(cases)
