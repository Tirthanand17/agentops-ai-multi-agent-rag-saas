from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TextChunk:
    chunk_id: str
    workspace_id: str
    source_id: str
    source_name: str
    text: str
    position: int


def chunk_text(
    *,
    workspace_id: str,
    source_id: str,
    source_name: str,
    text: str,
    chunk_size: int = 700,
    overlap: int = 120,
) -> list[TextChunk]:
    clean = " ".join(text.split())
    if not clean:
        return []

    chunks: list[TextChunk] = []
    start = 0
    position = 0

    while start < len(clean):
        end = min(len(clean), start + chunk_size)

        if end < len(clean):
            sentence_break = clean.rfind(". ", start, end)
            if sentence_break > start + chunk_size // 2:
                end = sentence_break + 1

        piece = clean[start:end].strip()
        if piece:
            chunks.append(
                TextChunk(
                    chunk_id=f"{source_id}:{position}",
                    workspace_id=workspace_id,
                    source_id=source_id,
                    source_name=source_name,
                    text=piece,
                    position=position,
                )
            )
            position += 1

        if end >= len(clean):
            break

        start = max(end - overlap, start + 1)

    return chunks
