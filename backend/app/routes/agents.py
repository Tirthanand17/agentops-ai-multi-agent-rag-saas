from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from ..agent_state import agent_runtime
from ..agents.models import AgentRun, TraceStep

router = APIRouter(prefix="/agents", tags=["agents"])


class AgentRunRequest(BaseModel):
    workspace_id: str = Field(min_length=1, max_length=100)
    request: str = Field(min_length=1, max_length=2000)


def serialize_trace(step: TraceStep) -> dict[str, object]:
    return {
        "step_id": step.step_id,
        "tool_name": step.tool_name,
        "rationale": step.rationale,
        "permission": step.permission,
        "status": step.status,
        "result": step.result,
        "error": step.error,
    }


def serialize_run(run: AgentRun) -> dict[str, object]:
    return {
        "run_id": run.run_id,
        "workspace_id": run.workspace_id,
        "request": run.request,
        "status": run.status,
        "final_response": run.final_response,
        "trace": [serialize_trace(step) for step in run.trace],
    }


@router.get("/tools")
def tools() -> dict[str, object]:
    return {
        "protocol": "mcp-style-local-v1",
        "tools": [
            {
                "name": spec.name,
                "description": spec.description,
                "permission": spec.permission,
                "input_schema": spec.input_schema,
            }
            for spec in agent_runtime.registry.specs()
        ],
    }


@router.post("/run")
def run_agent(request: AgentRunRequest) -> dict[str, object]:
    run = agent_runtime.start(
        workspace_id=request.workspace_id,
        request=request.request,
    )
    return serialize_run(run)


@router.get("/runs")
def list_runs() -> list[dict[str, object]]:
    return [serialize_run(run) for run in agent_runtime.list_runs()]


@router.get("/runs/{run_id}")
def get_run(run_id: str) -> dict[str, object]:
    run = agent_runtime.get(run_id)
    if run is None:
        raise HTTPException(status_code=404, detail="Agent run not found.")
    return serialize_run(run)


@router.post("/runs/{run_id}/approve/{step_id}")
def approve(run_id: str, step_id: str) -> dict[str, object]:
    run = agent_runtime.get(run_id)
    if run is None:
        raise HTTPException(status_code=404, detail="Agent run not found.")

    if step_id not in {step.step_id for step in run.plan}:
        raise HTTPException(status_code=404, detail="Agent step not found.")

    updated = agent_runtime.approve(run_id=run_id, step_id=step_id)
    return serialize_run(updated)
