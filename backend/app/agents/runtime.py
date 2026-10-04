from __future__ import annotations

from uuid import uuid4

from .models import (
    AgentRun,
    PermissionLevel,
    RunStatus,
    StepStatus,
    TraceStep,
)
from .planner import DemoPlanner
from .tools import ToolRegistry


class AgentRuntime:
    def __init__(
        self,
        *,
        registry: ToolRegistry,
        planner: DemoPlanner | None = None,
    ) -> None:
        self.registry = registry
        self.planner = planner or DemoPlanner()
        self.runs: dict[str, AgentRun] = {}

    def start(self, *, workspace_id: str, request: str) -> AgentRun:
        run = AgentRun(
            run_id=uuid4().hex[:12],
            workspace_id=workspace_id,
            request=request,
            plan=self.planner.plan(request),
        )
        self.runs[run.run_id] = run
        return self._continue(run)

    def get(self, run_id: str) -> AgentRun | None:
        return self.runs.get(run_id)

    def list_runs(self) -> list[AgentRun]:
        return list(self.runs.values())[::-1]

    def approve(self, *, run_id: str, step_id: str) -> AgentRun:
        run = self.runs[run_id]
        run.approved_steps.add(step_id)
        return self._continue(run)

    def _trace_for_step(self, run: AgentRun, step_id: str) -> TraceStep | None:
        return next((item for item in run.trace if item.step_id == step_id), None)

    def _continue(self, run: AgentRun) -> AgentRun:
        run.status = RunStatus.RUNNING

        for step in run.plan:
            existing = self._trace_for_step(run, step.step_id)
            if existing and existing.status == StepStatus.COMPLETED:
                continue

            tool = self.registry.get(step.tool_name)
            if tool is None:
                trace = existing or TraceStep(
                    step_id=step.step_id,
                    tool_name=step.tool_name,
                    rationale=step.rationale,
                    permission=PermissionLevel.READ,
                )
                trace.status = StepStatus.FAILED
                trace.error = "Tool not found."
                if existing is None:
                    run.trace.append(trace)
                run.status = RunStatus.FAILED
                return run

            trace = existing or TraceStep(
                step_id=step.step_id,
                tool_name=step.tool_name,
                rationale=step.rationale,
                permission=tool.permission,
            )
            if existing is None:
                run.trace.append(trace)

            if (
                tool.permission == PermissionLevel.WRITE
                and step.step_id not in run.approved_steps
            ):
                trace.status = StepStatus.AWAITING_APPROVAL
                run.status = RunStatus.AWAITING_APPROVAL
                run.final_response = (
                    "A write action is ready but requires human approval."
                )
                return run

            try:
                trace.status = StepStatus.RUNNING
                arguments = tool.validate(step.arguments)
                trace.result = tool.execute(
                    workspace_id=run.workspace_id,
                    arguments=arguments,
                )
                trace.status = StepStatus.COMPLETED
                trace.error = None
            except Exception as exc:
                trace.status = StepStatus.FAILED
                trace.error = str(exc)
                run.status = RunStatus.FAILED
                run.final_response = "Agent execution failed safely."
                return run

        run.status = RunStatus.COMPLETED
        run.final_response = self._summarize(run)
        return run

    def _summarize(self, run: AgentRun) -> str:
        completed = [step for step in run.trace if step.status == StepStatus.COMPLETED]
        if not completed:
            return "No tool output was produced."

        if "renewal" in run.request.lower() and "risk" in run.request.lower():
            crm_result = next(
                (
                    step.result
                    for step in completed
                    if step.tool_name == "customer_lookup"
                    and isinstance(step.result, dict)
                ),
                None,
            )
            if crm_result and crm_result.get("found", True):
                return (
                    f"{crm_result['name']} has a health score of "
                    f"{crm_result['health_score']}, {crm_result['open_tickets']} open "
                    f"tickets, and renews in {crm_result['renewal_days']} days. "
                    "The execution trace includes grounded support-policy evidence."
                )

        last = completed[-1]
        return f"Agent completed {len(completed)} tool step(s). Last result: {last.result}"
