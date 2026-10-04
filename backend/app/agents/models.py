from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class PermissionLevel(StrEnum):
    READ = "read"
    WRITE = "write"


class StepStatus(StrEnum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    AWAITING_APPROVAL = "awaiting_approval"
    FAILED = "failed"


class RunStatus(StrEnum):
    RUNNING = "running"
    COMPLETED = "completed"
    AWAITING_APPROVAL = "awaiting_approval"
    FAILED = "failed"


@dataclass(frozen=True)
class ToolSpec:
    name: str
    description: str
    permission: PermissionLevel
    input_schema: dict[str, Any]


@dataclass(frozen=True)
class PlanStep:
    step_id: str
    tool_name: str
    arguments: dict[str, Any]
    rationale: str


@dataclass
class TraceStep:
    step_id: str
    tool_name: str
    rationale: str
    permission: PermissionLevel
    status: StepStatus = StepStatus.PENDING
    result: Any = None
    error: str | None = None


@dataclass
class AgentRun:
    run_id: str
    workspace_id: str
    request: str
    plan: list[PlanStep]
    trace: list[TraceStep] = field(default_factory=list)
    status: RunStatus = RunStatus.RUNNING
    final_response: str | None = None
    approved_steps: set[str] = field(default_factory=set)
