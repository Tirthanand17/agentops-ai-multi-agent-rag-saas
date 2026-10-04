from __future__ import annotations

from .agents.factory import create_agent_runtime
from .state import rag_service

agent_runtime = create_agent_runtime(rag_service)
