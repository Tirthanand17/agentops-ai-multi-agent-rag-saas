from app.agents.factory import create_agent_runtime
from app.agents.models import RunStatus, StepStatus
from app.rag.demo import DEMO_WORKSPACE, create_demo_rag_service


def make_runtime():
    return create_agent_runtime(create_demo_rag_service())


def test_registry_exposes_mcp_style_tool_metadata() -> None:
    runtime = make_runtime()
    specs = {spec.name: spec for spec in runtime.registry.specs()}

    assert "knowledge_search" in specs
    assert "create_ticket" in specs
    assert specs["create_ticket"].permission == "write"
    assert "properties" in specs["knowledge_search"].input_schema


def test_read_only_agent_run_completes_with_trace() -> None:
    runtime = make_runtime()
    run = runtime.start(
        workspace_id=DEMO_WORKSPACE,
        request="What is the refund window?",
    )

    assert run.status == RunStatus.COMPLETED
    assert run.trace
    assert run.trace[0].tool_name == "knowledge_search"
    assert run.trace[0].status == StepStatus.COMPLETED


def test_write_tool_waits_for_human_approval() -> None:
    runtime = make_runtime()
    run = runtime.start(
        workspace_id=DEMO_WORKSPACE,
        request="Escalate Acme and create a support ticket.",
    )

    assert run.status == RunStatus.AWAITING_APPROVAL
    pending = run.trace[-1]
    assert pending.tool_name == "create_ticket"
    assert pending.status == StepStatus.AWAITING_APPROVAL
    assert pending.result is None


def test_approved_write_tool_executes_and_completes() -> None:
    runtime = make_runtime()
    run = runtime.start(
        workspace_id=DEMO_WORKSPACE,
        request="Escalate Acme and create a support ticket.",
    )

    pending_step = run.trace[-1]
    updated = runtime.approve(
        run_id=run.run_id,
        step_id=pending_step.step_id,
    )

    assert updated.status == RunStatus.COMPLETED
    completed = updated.trace[-1]
    assert completed.status == StepStatus.COMPLETED
    assert completed.result["status"] == "created-demo"


def test_customer_lookup_plan_for_renewal_risk() -> None:
    runtime = make_runtime()
    run = runtime.start(
        workspace_id=DEMO_WORKSPACE,
        request="Summarize renewal risk for Acme.",
    )

    assert run.status == RunStatus.COMPLETED
    assert [step.tool_name for step in run.trace] == [
        "knowledge_search",
        "customer_lookup",
    ]
    assert "Acme Retail" in (run.final_response or "")
