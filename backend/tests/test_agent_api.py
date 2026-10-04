from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_tools_endpoint_exposes_write_permissions() -> None:
    response = client.get("/api/v1/agents/tools")
    assert response.status_code == 200
    payload = response.json()
    tools = {tool["name"]: tool for tool in payload["tools"]}
    assert tools["create_ticket"]["permission"] == "write"
    assert tools["knowledge_search"]["permission"] == "read"


def test_agent_api_requires_and_accepts_approval() -> None:
    start = client.post(
        "/api/v1/agents/run",
        json={
            "workspace_id": "demo-retail",
            "request": "Escalate Acme and create a support ticket.",
        },
    )
    assert start.status_code == 200
    run = start.json()
    assert run["status"] == "awaiting_approval"

    pending = run["trace"][-1]
    assert pending["tool_name"] == "create_ticket"
    assert pending["status"] == "awaiting_approval"
    assert pending["result"] is None

    approved = client.post(
        f"/api/v1/agents/runs/{run['run_id']}/approve/{pending['step_id']}"
    )
    assert approved.status_code == 200
    updated = approved.json()
    assert updated["status"] == "completed"
    assert updated["trace"][-1]["result"]["status"] == "created-demo"


def test_agent_evaluation_endpoint_passes() -> None:
    response = client.get("/api/v1/evaluation/agents")
    assert response.status_code == 200
    payload = response.json()
    assert payload["passed"] is True
    assert payload["tool_selection_accuracy"] == 1.0
