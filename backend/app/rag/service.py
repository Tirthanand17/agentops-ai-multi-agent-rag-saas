from __future__ import annotations

from dataclasses import dataclass
from uuid import uuid4

from .chunking import chunk_text
from .embeddings import Embedder, HashingEmbedder
from .store import InMemoryVectorStore, SearchHit


@dataclass(frozen=True)
class Citation:
    source_id: str
    source_name: str
    chunk_id: str
    score: float
    excerpt: str


@dataclass(frozen=True)
class RAGAnswer:
    answer: str
    citations: list[Citation]


class RAGService:
    def __init__(
        self,
        *,
        embedder: Embedder | None = None,
        store: InMemoryVectorStore | None = None,
    ) -> None:
        self.embedder = embedder or HashingEmbedder()
        self.store = store or InMemoryVectorStore()

    def ingest(
        self,
        *,
        workspace_id: str,
        source_name: str,
        text: str,
        source_id: str | None = None,
    ) -> dict[str, object]:
        resolved_source_id = source_id or uuid4().hex[:12]
        chunks = chunk_text(
            workspace_id=workspace_id,
            source_id=resolved_source_id,
            source_name=source_name,
            text=text,
        )
        if not chunks:
            raise ValueError("Document contains no indexable text.")

        vectors = self.embedder.encode([chunk.text for chunk in chunks])
        self.store.add(chunks, vectors)

        return {
            "workspace_id": workspace_id,
            "source_id": resolved_source_id,
            "source_name": source_name,
            "chunks": len(chunks),
        }

    def search(
        self,
        *,
        workspace_id: str,
        query: str,
        top_k: int = 4,
    ) -> list[SearchHit]:
        vector = self.embedder.encode([query])[0]
        return self.store.search(
            workspace_id=workspace_id,
            query_vector=vector,
            top_k=top_k,
        )

    def ask(
        self,
        *,
        workspace_id: str,
        question: str,
        top_k: int = 4,
    ) -> RAGAnswer:
        hits = self.search(
            workspace_id=workspace_id,
            query=question,
            top_k=top_k,
        )

        if not hits:
            return RAGAnswer(
                answer="I could not find grounded evidence in this workspace.",
                citations=[],
            )

        useful = [hit for hit in hits if hit.score > 0]
        if not useful:
            return RAGAnswer(
                answer="I could not find grounded evidence in this workspace.",
                citations=[],
            )

        citations = [
            Citation(
                source_id=hit.chunk.source_id,
                source_name=hit.chunk.source_name,
                chunk_id=hit.chunk.chunk_id,
                score=round(hit.score, 4),
                excerpt=hit.chunk.text[:280],
            )
            for hit in useful
        ]

        evidence = " ".join(hit.chunk.text for hit in useful[:3])
        answer = (
            "Grounded answer from the indexed workspace knowledge: "
            + evidence
        )

        return RAGAnswer(answer=answer, citations=citations)

    def sources(self, workspace_id: str) -> list[dict[str, object]]:
        return self.store.sources(workspace_id)
