from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from ..state import rag_service

router = APIRouter(prefix="/knowledge", tags=["knowledge"])


class IngestRequest(BaseModel):
    workspace_id: str = Field(min_length=1)
    source_name: str = Field(min_length=1)
    text: str = Field(min_length=1)


class SearchRequest(BaseModel):
    workspace_id: str = Field(min_length=1)
    query: str = Field(min_length=1)
    top_k: int = Field(default=4, ge=1, le=10)


class AskRequest(BaseModel):
    workspace_id: str = Field(min_length=1)
    question: str = Field(min_length=1)
    top_k: int = Field(default=4, ge=1, le=10)


@router.post("/ingest")
def ingest(request: IngestRequest) -> dict[str, object]:
    try:
        return rag_service.ingest(
            workspace_id=request.workspace_id,
            source_name=request.source_name,
            text=request.text,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/{workspace_id}/sources")
def sources(workspace_id: str) -> list[dict[str, object]]:
    return rag_service.sources(workspace_id)


@router.post("/search")
def search(request: SearchRequest) -> dict[str, object]:
    hits = rag_service.search(
        workspace_id=request.workspace_id,
        query=request.query,
        top_k=request.top_k,
    )
    return {
        "workspace_id": request.workspace_id,
        "query": request.query,
        "hits": [
            {
                "source_id": hit.chunk.source_id,
                "source_name": hit.chunk.source_name,
                "chunk_id": hit.chunk.chunk_id,
                "score": round(hit.score, 4),
                "text": hit.chunk.text,
            }
            for hit in hits
        ],
    }


@router.post("/ask")
def ask(request: AskRequest) -> dict[str, object]:
    result = rag_service.ask(
        workspace_id=request.workspace_id,
        question=request.question,
        top_k=request.top_k,
    )
    return {
        "workspace_id": request.workspace_id,
        "question": request.question,
        "answer": result.answer,
        "citations": [
            {
                "source_id": citation.source_id,
                "source_name": citation.source_name,
                "chunk_id": citation.chunk_id,
                "score": citation.score,
                "excerpt": citation.excerpt,
            }
            for citation in result.citations
        ],
    }
