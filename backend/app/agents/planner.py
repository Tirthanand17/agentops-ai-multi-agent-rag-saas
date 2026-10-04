from __future__ import annotations

from .models import PlanStep


class DemoPlanner:
    """Deterministic local planner; replaceable by an LLM planner adapter later."""

    def plan(self, request: str) -> list[PlanStep]:
        text = request.strip()
        lowered = text.lower()

        if "renewal" in lowered and "risk" in lowered:
            customer_name = "Acme" if "acme" in lowered else text
            return [
                PlanStep(
                    step_id="step-1",
                    tool_name="knowledge_search",
                    arguments={"query": "support escalation enterprise response policy", "top_k": 2},
                    rationale="Retrieve policy context that can affect account risk.",
                ),
                PlanStep(
                    step_id="step-2",
                    tool_name="customer_lookup",
                    arguments={"customer_name": customer_name},
                    rationale="Retrieve current synthetic CRM account indicators.",
                ),
            ]

        if "ticket" in lowered or "escalat" in lowered:
            customer_name = "Acme" if "acme" in lowered else "Customer"
            return [
                PlanStep(
                    step_id="step-1",
                    tool_name="knowledge_search",
                    arguments={"query": "critical service outage escalation policy", "top_k": 2},
                    rationale="Retrieve the relevant support policy before taking action.",
                ),
                PlanStep(
                    step_id="step-2",
                    tool_name="create_ticket",
                    arguments={
                        "title": text,
                        "priority": "high",
                        "customer_name": customer_name,
                    },
                    rationale="Create the requested escalation only after human approval.",
                ),
            ]

        if "order" in lowered:
            order_id = "ORD-1042" if "1042" in lowered else "ORD-1048"
            return [
                PlanStep(
                    step_id="step-1",
                    tool_name="order_lookup",
                    arguments={"order_id": order_id},
                    rationale="Retrieve order status from the synthetic operations dataset.",
                )
            ]

        return [
            PlanStep(
                step_id="step-1",
                tool_name="knowledge_search",
                arguments={"query": text, "top_k": 3},
                rationale="Ground the response in workspace knowledge.",
            )
        ]
