# Deployment

AgentOps AI is live on a zero-cost public portfolio deployment on Render.

## Chosen public-demo topology

- Frontend: Render Static Site, built as a Next.js static export.
- Backend: Render Free Python web service running FastAPI.
- Region: Singapore for the API service.
- Data: seeded synthetic in-memory demo state.
- AI provider: `demo` mode; no paid LLM credentials are required.
- Infrastructure definition: root `render.yaml`.

This is intentionally a portfolio/demo deployment, not a claim of production customer usage.

## Why the demo is stateless

The current application does not persist agent or RAG state through the configured `DATABASE_URL`; the seeded demo stores are in memory. A free Render web service has an ephemeral filesystem and can restart after idle periods, so the public demo is designed to recreate its synthetic workspace on startup.

Do not provision a database merely to claim PostgreSQL. Persistent PostgreSQL/pgvector plus real authentication/RBAC should be added when those components are actually wired into the product.

## Free-tier behavior

Render Free web services can spin down after 15 minutes without inbound traffic. The next request can take about a minute while the API wakes up. The static frontend remains CDN-hosted.

## Live services

### Backend

Service name:

`agentops-ai-api-tirthanand17`

Live URL:

`https://agentops-ai-api-tirthanand17.onrender.com`

Runtime:
- Python 3.12.11
- FastAPI / Uvicorn
- Free compute
- Singapore
- health check: `/ready`

### Frontend

Service name:

`agentops-ai-demo-tirthanand17`

Live URL:

`https://agentops-ai-demo-tirthanand17.onrender.com`

The live frontend build sets `STATIC_EXPORT=true` and `NEXT_PUBLIC_API_BASE_URL=https://agentops-ai-api-tirthanand17.onrender.com`. The backend `ALLOWED_ORIGINS` setting is restricted to the deployed frontend origin.

The root `render.yaml` remains a reproducible Blueprint-style deployment definition and includes an alternative same-origin rewrite topology. Static-export security headers can be applied at the Render edge because Next.js server response headers are not available in static-export mode.

## Local validation

Backend:

```bash
cd backend
python -m pip install -r requirements.txt
python -m pytest -q
```

Frontend standalone mode:

```bash
cd frontend
npm ci
npm run lint
npm run build
```

Frontend Render/static-export mode:

```bash
cd frontend
STATIC_EXPORT=true NEXT_PUBLIC_STATIC_PROXY=true npm run build
```

A successful static build creates `frontend/out`.

## Public smoke-test checklist

1. Open the frontend HTTPS URL.
2. Allow for one cold start if the free API has been idle.
3. Confirm the API status card becomes Online.
4. Run: `What is the refund window?`
5. Confirm a grounded knowledge-search result is returned.
6. Run: `Summarize renewal risk for Acme.`
7. Confirm the trace contains knowledge search + customer lookup.
8. Run: `Escalate Acme and create a support ticket.`
9. Verify the write step stops for explicit human approval.
10. Approve it and verify the synthetic ticket result completes.
11. Confirm RAG evaluation and agent-routing cards show their seeded evaluation results.
12. Test microphone input in a supported browser after granting permission.
13. Test spoken response output.
14. Check `/ready` and the backend `/docs` endpoint.
15. Verify no secrets or real client data are exposed.

## Security and truthfulness

- Synthetic data only.
- No API secrets are required for demo mode.
- No real write integration is executed.
- Write actions are approval-gated.
- Request sizes are bounded.
- Frontend and backend send baseline security headers.
- The demo does not claim persistent storage, production users, or client usage.

## Future production hardening

Before real customer use:
- add persistent PostgreSQL/pgvector storage,
- add real authentication and tenant-aware RBAC,
- persist audit/trace records,
- add rate limiting,
- add structured application metrics/logging,
- introduce migrations and backup/restore procedures,
- run deployment-specific security testing.
