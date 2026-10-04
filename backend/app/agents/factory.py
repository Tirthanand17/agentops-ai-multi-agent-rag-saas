from __future__ import annotations

from ..rag.service import RAGService
from .runtime import AgentRuntime
from .tools import (
    CreateTicketTool,
    CustomerLookupTool,
    KnowledgeSearchTool,
    OrderLookupTool,
    RiskScoreTool,
    ToolRegistry,
)


def create_agent_runtime(rag_service: RAGService) -> AgentRuntime:
    registry = ToolRegistry(
        [
            KnowledgeSearchTool(rag_service),
            CustomerLookupTool(),
            OrderLookupTool(),
            RiskScoreTool(),
            CreateTicketTool(),
        ]
    )
    return AgentRuntime(registry=registry)
