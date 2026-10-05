from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .routes.agents import router as agents_router
from .routes.evaluation import router as evaluation_router
from .routes.health import router as health_router
from .routes.knowledge import router as knowledge_router
from .routes.workspaces import router as workspaces_router

app = FastAPI(
    title="AgentOps AI API",
    version="0.4.0",
    description="Backend for the AgentOps AI multi-agent RAG SaaS portfolio project.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "camera=(), geolocation=(), microphone=(self)"
    return response


app.include_router(health_router)
app.include_router(workspaces_router, prefix="/api/v1")
app.include_router(knowledge_router, prefix="/api/v1")
app.include_router(agents_router, prefix="/api/v1")
app.include_router(evaluation_router, prefix="/api/v1")


@app.get("/")
def root() -> dict[str, str]:
    return {
        "name": "AgentOps AI API",
        "status": "ready",
        "docs": "/docs",
    }
