from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/workspaces", tags=["workspaces"])


class WorkspaceSummary(BaseModel):
    id: str
    name: str
    plan: str
    documents: int
    agents: int
    updated_at: datetime


DEMO_WORKSPACES = [
    WorkspaceSummary(
        id="demo-retail",
        name="Northstar Commerce",
        plan="Portfolio Demo",
        documents=12,
        agents=3,
        updated_at=datetime(2026, 10, 4, 12, 0, tzinfo=timezone.utc),
    ),
    WorkspaceSummary(
        id="demo-services",
        name="Atlas Field Services",
        plan="Portfolio Demo",
        documents=8,
        agents=2,
        updated_at=datetime(2026, 10, 4, 10, 30, tzinfo=timezone.utc),
    ),
]


@router.get("", response_model=list[WorkspaceSummary])
def list_workspaces() -> list[WorkspaceSummary]:
    return DEMO_WORKSPACES
