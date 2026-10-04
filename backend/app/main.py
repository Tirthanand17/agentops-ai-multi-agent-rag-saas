from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .routes.health import router as health_router
from .routes.workspaces import router as workspaces_router

app = FastAPI(
    title="AgentOps AI API",
    version="0.1.0",
    description="Backend for the AgentOps AI multi-agent RAG SaaS portfolio project.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(workspaces_router, prefix="/api/v1")


@app.get("/")
def root() -> dict[str, str]:
    return {
        "name": "AgentOps AI API",
        "status": "ready",
        "docs": "/docs",
    }
