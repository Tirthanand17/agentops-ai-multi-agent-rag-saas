from __future__ import annotations

from .evaluation import RetrievalCase
from .service import RAGService


DEMO_WORKSPACE = "demo-retail"

DEMO_DOCUMENTS = [
    {
        "source_id": "support-policy",
        "source_name": "Support Policies",
        "text": (
            "Priority support tickets from enterprise customers must receive an initial "
            "response within two business hours. Standard customers receive an initial "
            "response within one business day. Critical service outages should be "
            "escalated immediately to the incident response lead."
        ),
    },
    {
        "source_id": "returns-policy",
        "source_name": "Returns & Refunds",
        "text": (
            "Customers may request a refund within 30 calendar days of purchase when a "
            "valid receipt is available. Digital services already fully consumed are not "
            "eligible for refund. Approved refunds are returned to the original payment method."
        ),
    },
    {
        "source_id": "shipping-policy",
        "source_name": "Shipping Guide",
        "text": (
            "Standard shipping takes three to five business days. Express shipping takes "
            "one to two business days. Orders above 100 dollars qualify for free standard shipping."
        ),
    },
]


DEMO_EVAL_CASES = [
    RetrievalCase(
        workspace_id=DEMO_WORKSPACE,
        query="How quickly should enterprise support tickets receive a response?",
        expected_source_id="support-policy",
    ),
    RetrievalCase(
        workspace_id=DEMO_WORKSPACE,
        query="How long does express delivery take?",
        expected_source_id="shipping-policy",
    ),
    RetrievalCase(
        workspace_id=DEMO_WORKSPACE,
        query="What is the refund window?",
        expected_source_id="returns-policy",
    ),
]


def create_demo_rag_service() -> RAGService:
    service = RAGService()
    for document in DEMO_DOCUMENTS:
        service.ingest(
            workspace_id=DEMO_WORKSPACE,
            source_id=document["source_id"],
            source_name=document["source_name"],
            text=document["text"],
        )
    return service
