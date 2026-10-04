from __future__ import annotations

from dataclasses import dataclass

from .runtime import AgentRuntime


@dataclass(frozen=True)
class AgentEvalCase:
    request: str
    expected_tools: tuple[str, ...]


def tool_selection_accuracy(
    runtime: AgentRuntime,
    workspace_id: str,
    cases: list[AgentEvalCase],
) -> float:
    if not cases:
        return 0.0

    correct = 0
    for case in cases:
        plan = runtime.planner.plan(case.request)
        tools = tuple(step.tool_name for step in plan)
        correct += int(tools == case.expected_tools)

    return correct / len(cases)
