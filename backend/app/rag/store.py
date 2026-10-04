from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .chunking import TextChunk


@dataclass(frozen=True)
class SearchHit:
    chunk: TextChunk
    score: float


class InMemoryVectorStore:
    """Tenant-isolated vector store used for local development and tests."""

    def __init__(self) -> None:
        self._chunks: list[TextChunk] = []
        self._vectors: list[np.ndarray] = []

    def add(self, chunks: list[TextChunk], vectors: np.ndarray) -> None:
        if len(chunks) != len(vectors):
            raise ValueError("Chunks and vectors must have identical lengths.")

        for chunk, vector in zip(chunks, vectors, strict=True):
            self._chunks.append(chunk)
            self._vectors.append(np.asarray(vector, dtype=np.float32))

    def sources(self, workspace_id: str) -> list[dict[str, object]]:
        grouped: dict[str, dict[str, object]] = {}
        for chunk in self._chunks:
            if chunk.workspace_id != workspace_id:
                continue
            record = grouped.setdefault(
                chunk.source_id,
                {
                    "source_id": chunk.source_id,
                    "source_name": chunk.source_name,
                    "chunks": 0,
                },
            )
            record["chunks"] = int(record["chunks"]) + 1
        return list(grouped.values())

    def search(
        self,
        *,
        workspace_id: str,
        query_vector: np.ndarray,
        top_k: int,
    ) -> list[SearchHit]:
        candidates: list[tuple[TextChunk, np.ndarray]] = [
            (chunk, vector)
            for chunk, vector in zip(self._chunks, self._vectors, strict=True)
            if chunk.workspace_id == workspace_id
        ]

        if not candidates:
            return []

        q = np.asarray(query_vector, dtype=np.float32)
        q_norm = float(np.linalg.norm(q))
        if q_norm == 0:
            return []

        scored: list[SearchHit] = []
        for chunk, vector in candidates:
            denominator = q_norm * float(np.linalg.norm(vector))
            score = 0.0 if denominator == 0 else float(np.dot(q, vector) / denominator)
            scored.append(SearchHit(chunk=chunk, score=score))

        scored.sort(key=lambda hit: hit.score, reverse=True)
        return scored[:top_k]
