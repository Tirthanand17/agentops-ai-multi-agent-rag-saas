# Decision Log

## 2026-10-04 — Project selection

Selected a full-stack AI SaaS over a pure voice-AI project.

Reason:
Current Upwork demand repeatedly asks for production-ready combinations of Next.js/React, FastAPI, PostgreSQL, RAG, vector databases, AI agents, tool calling, MCP, API integrations, Docker, authentication, and cloud deployment.

Voice AI remains a planned extension because many voice-specific jobs require prior live telephony deployment evidence.


## 2026-10-05 — Public demo deployment topology

Selected Render for the public portfolio demo:
- free static site for the Next.js frontend
- free Python web service for FastAPI
- Singapore API region
- same-origin static-site rewrites to proxy API calls
- synthetic in-memory demo state

Reason:
- Render explicitly supports free static sites and free Python web services for hobby/prototype use.
- A static frontend avoids consuming a second free compute instance.
- The current code does not persist runtime state through DATABASE_URL, so provisioning PostgreSQL before wiring persistence would be misleading.
- Free Render Postgres expires after 30 days, which is a poor default for a durable portfolio URL.

Production PostgreSQL/pgvector and authentication/RBAC remain architectural targets and will only be claimed after they are implemented in runtime behavior.
