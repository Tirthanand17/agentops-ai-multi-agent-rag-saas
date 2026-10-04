from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel, Field

from ..rag.service import RAGService
from .business_data import DEMO_CUSTOMERS, DEMO_ORDERS
from .models import PermissionLevel, ToolSpec


class KnowledgeSearchInput(BaseModel):
    query: str = Field(min_length=1)
    top_k: int = Field(default=3, ge=1, le=8)


class CustomerLookupInput(BaseModel):
    customer_name: str = Field(min_length=1)


class OrderLookupInput(BaseModel):
    order_id: str = Field(min_length=1)


class RiskScoreInput(BaseModel):
    health_score: int = Field(ge=0, le=100)
    open_tickets: int = Field(ge=0)
    renewal_days: int = Field(ge=0)


class CreateTicketInput(BaseModel):
    title: str = Field(min_length=3)
    priority: str = Field(default="medium")
    customer_name: str = Field(min_length=1)


class Tool(ABC):
    name: str
    description: str
    permission: PermissionLevel
    input_model: type[BaseModel]

    @property
    def spec(self) -> ToolSpec:
        return ToolSpec(
            name=self.name,
            description=self.description,
            permission=self.permission,
            input_schema=self.input_model.model_json_schema(),
        )

    def validate(self, arguments: dict[str, Any]) -> BaseModel:
        return self.input_model.model_validate(arguments)

    @abstractmethod
    def execute(
        self,
        *,
        workspace_id: str,
        arguments: BaseModel,
    ) -> dict[str, Any]:
        raise NotImplementedError


class KnowledgeSearchTool(Tool):
    name = "knowledge_search"
    description = "Search tenant-scoped company knowledge and return cited evidence."
    permission = PermissionLevel.READ
    input_model = KnowledgeSearchInput

    def __init__(self, rag_service: RAGService) -> None:
        self.rag_service = rag_service

    def execute(
        self,
        *,
        workspace_id: str,
        arguments: BaseModel,
    ) -> dict[str, Any]:
        data = KnowledgeSearchInput.model_validate(arguments)
        hits = self.rag_service.search(
            workspace_id=workspace_id,
            query=data.query,
            top_k=data.top_k,
        )
        return {
            "hits": [
                {
                    "source_id": hit.chunk.source_id,
                    "source_name": hit.chunk.source_name,
                    "chunk_id": hit.chunk.chunk_id,
                    "score": round(hit.score, 4),
                    "text": hit.chunk.text,
                }
                for hit in hits
            ]
        }


class CustomerLookupTool(Tool):
    name = "customer_lookup"
    description = "Look up synthetic CRM customer data within the current workspace."
    permission = PermissionLevel.READ
    input_model = CustomerLookupInput

    def execute(
        self,
        *,
        workspace_id: str,
        arguments: BaseModel,
    ) -> dict[str, Any]:
        data = CustomerLookupInput.model_validate(arguments)
        customers = DEMO_CUSTOMERS.get(workspace_id, {})
        needle = data.customer_name.strip().lower()

        for key, customer in customers.items():
            if needle in key.lower() or needle in customer["name"].lower():
                return dict(customer)

        return {"found": False, "customer_name": data.customer_name}


class OrderLookupTool(Tool):
    name = "order_lookup"
    description = "Look up a synthetic order in the current workspace."
    permission = PermissionLevel.READ
    input_model = OrderLookupInput

    def execute(
        self,
        *,
        workspace_id: str,
        arguments: BaseModel,
    ) -> dict[str, Any]:
        data = OrderLookupInput.model_validate(arguments)
        order = DEMO_ORDERS.get(workspace_id, {}).get(data.order_id.upper())
        if order is None:
            return {"found": False, "order_id": data.order_id}
        return dict(order)


class RiskScoreTool(Tool):
    name = "risk_score"
    description = "Calculate a transparent renewal-risk score from CRM indicators."
    permission = PermissionLevel.READ
    input_model = RiskScoreInput

    def execute(
        self,
        *,
        workspace_id: str,
        arguments: BaseModel,
    ) -> dict[str, Any]:
        del workspace_id
        data = RiskScoreInput.model_validate(arguments)

        health_component = (100 - data.health_score) * 0.55
        ticket_component = min(data.open_tickets * 7, 28)
        urgency_component = max(0, 30 - min(data.renewal_days, 30)) * 0.57
        score = min(100, round(health_component + ticket_component + urgency_component, 1))

        label = "high" if score >= 65 else "medium" if score >= 35 else "low"
        return {
            "risk_score": score,
            "risk_label": label,
            "method": "transparent weighted demo score",
        }


class CreateTicketTool(Tool):
    name = "create_ticket"
    description = "Create a synthetic support ticket. This write action requires approval."
    permission = PermissionLevel.WRITE
    input_model = CreateTicketInput

    def execute(
        self,
        *,
        workspace_id: str,
        arguments: BaseModel,
    ) -> dict[str, Any]:
        data = CreateTicketInput.model_validate(arguments)
        return {
            "ticket_id": f"TKT-{abs(hash((workspace_id, data.title))) % 9000 + 1000}",
            "workspace_id": workspace_id,
            "title": data.title,
            "priority": data.priority,
            "customer_name": data.customer_name,
            "status": "created-demo",
        }


class ToolRegistry:
    def __init__(self, tools: list[Tool]) -> None:
        self._tools = {tool.name: tool for tool in tools}

    def get(self, name: str) -> Tool | None:
        return self._tools.get(name)

    def specs(self) -> list[ToolSpec]:
        return [tool.spec for tool in self._tools.values()]
