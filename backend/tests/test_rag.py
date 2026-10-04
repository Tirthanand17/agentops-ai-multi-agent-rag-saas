from app.rag.demo import DEMO_EVAL_CASES, DEMO_WORKSPACE, create_demo_rag_service
from app.rag.evaluation import retrieval_hit_rate
from app.rag.service import RAGService


def test_demo_retrieval_finds_shipping_source() -> None:
    service = create_demo_rag_service()
    hits = service.search(
        workspace_id=DEMO_WORKSPACE,
        query="How long does express delivery take?",
        top_k=1,
    )
    assert hits
    assert hits[0].chunk.source_id == "shipping-policy"


def test_workspace_isolation() -> None:
    service = RAGService()
    service.ingest(
        workspace_id="alpha",
        source_id="alpha-source",
        source_name="Alpha",
        text="Alpha company uses a seven day review period.",
    )
    service.ingest(
        workspace_id="beta",
        source_id="beta-source",
        source_name="Beta",
        text="Beta company uses a fourteen day review period.",
    )

    hits = service.search(
        workspace_id="alpha",
        query="What is the review period?",
        top_k=10,
    )

    assert hits
    assert {hit.chunk.workspace_id for hit in hits} == {"alpha"}


def test_ask_returns_citations() -> None:
    service = create_demo_rag_service()
    answer = service.ask(
        workspace_id=DEMO_WORKSPACE,
        question="What is the refund window?",
        top_k=2,
    )

    assert answer.citations
    assert answer.citations[0].source_id == "returns-policy"
    assert "30" in answer.answer


def test_retrieval_evaluation_passes_demo_cases() -> None:
    service = create_demo_rag_service()
    score = retrieval_hit_rate(
        service,
        DEMO_EVAL_CASES,
        top_k=2,
    )
    assert score == 1.0
