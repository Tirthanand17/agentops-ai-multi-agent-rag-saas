# Deployment Preparation

AgentOps AI is designed to deploy without paid AI credentials in demo mode.

## Recommended topology

- Frontend: a Next.js-compatible host.
- Backend: any host that can run the backend Docker image.
- Database: PostgreSQL with pgvector when the persistent production store is enabled.
- AI provider: keep `LLM_PROVIDER=demo` for the public portfolio demo, or supply a supported provider later.

No paid service should be enabled without explicit approval.

## Frontend environment

Copy `frontend/.env.example` to the host environment and set:

```text
NEXT_PUBLIC_API_BASE_URL=https://your-api.example.com
```

The URL must point to the deployed FastAPI service.

## Backend environment

Start from `backend/.env.example`.

For a public deployment, set at minimum:

```text
APP_ENV=production
DATABASE_URL=postgresql+psycopg://...
ALLOWED_ORIGINS=["https://your-frontend.example.com"]
LLM_PROVIDER=demo
```

Never commit real database passwords, API keys, tokens, or client data.

## Health endpoints

- `GET /health` — service liveness
- `GET /ready` — deployment readiness

The backend Docker image includes a health check against `/ready`.

## Build validation

Backend:

```bash
cd backend
python -m pip install -r requirements.txt
python -m pytest -q
```

Frontend:

```bash
cd frontend
npm ci
npm run lint
npm run build
```

Docker:

```bash
docker compose build
```

## Smoke-test checklist

1. Load the frontend over HTTPS.
2. Confirm the API status card is online.
3. Run a grounded knowledge search.
4. Run a read-only agent request.
5. Trigger a write workflow and verify it stops for approval.
6. Approve the demo write action and verify completion.
7. Run RAG and agent evaluation cards.
8. Test microphone capture in a supported browser after granting permission.
9. Test spoken response output.
10. Verify no secrets or real client data are exposed.

## Voice deployment note

Browser speech recognition and text-to-speech availability varies by browser and device. The UI detects support and falls back to text controls when voice APIs are unavailable. Microphone access requires a secure context (HTTPS on public deployments, with localhost allowed during development).

## Production follow-ups

Before using this project with real customers, replace in-memory/demo stores with persistent tenant-aware storage, add production authentication/RBAC, add rate limiting, configure structured logs/metrics, and perform a deployment-specific security review.
