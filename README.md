# AgentOps AI

**Multi-Agent RAG SaaS for Business Operations**

AgentOps AI is a production-style full-stack AI portfolio project designed to demonstrate the capabilities repeatedly requested in current Upwork AI SaaS roles: modern web development, RAG, AI agents, tool calling, vector search, multi-tenant architecture, APIs, evaluation, observability, and cloud deployment.

## Product concept

A business workspace where a team can:
- upload company documents and build a cited knowledge base
- chat with an AI copilot grounded in company data
- run tool-using AI agents for business operations
- review plans, tool calls, results, and confidence
- require human approval before sensitive actions
- inspect retrieval quality, latency, and agent traces
- use browser voice input/output
- manage multiple workspaces with tenant-aware isolation

## Planned stack

Frontend:
- Next.js, React, TypeScript, Tailwind CSS
- streaming chat UI
- dashboard and execution trace views

Backend:
- Python, FastAPI, Pydantic
- SSE streaming
- background job abstraction

AI:
- provider-neutral LLM adapter
- RAG with citations
- embeddings plus pgvector
- state-graph agent orchestration
- structured tool calling
- MCP-style tool registry
- retrieval and agent evaluation
- approval safeguards for actions

Data/platform:
- Supabase Auth
- PostgreSQL
- pgvector
- workspace and tenant isolation
- audit/event log
- optional Redis-compatible cache/queue

Delivery:
- Docker
- GitHub Actions
- Vercel frontend deployment
- container backend deployment
- Supabase database deployment

## High-level architecture

Browser / Next.js
 -> Auth + SSE
 -> FastAPI
    -> Workspace / RBAC
    -> RAG pipeline
    -> Agent runtime
    -> Business tools
    -> Evaluation / observability
 -> PostgreSQL / pgvector

## Portfolio outcome

The finished project will include:
1. public GitHub repository
2. live deployed web app
3. seeded demo workspace with synthetic data
4. architecture documentation
5. automated tests and CI
6. screenshots
7. short walkthrough video
8. natural-tone narration/audio
9. polished Upwork portfolio entry

## Current status

**Step 7 — browser voice interaction and deployment hardening complete.**

Validated locally:
- FastAPI test suite: 17 passed
- Next.js lint: passed
- Next.js production build: passed
- Production npm audit: 0 vulnerabilities
- Browser speech-to-text controls: implemented with graceful unsupported/permission fallback
- Browser text-to-speech response control: implemented
- API request-size validation: implemented
- Frontend and backend baseline security headers: implemented
- Backend readiness endpoint: implemented
- Docker health check and Docker build-ignore files: added
- Deployment environment templates and smoke-test guide: added

Existing integrated capabilities remain in place:
- live API health indicator
- RAG evaluation at 100% on the seeded demo fixture
- agent routing evaluation at 100% on the seeded demo fixture
- tenant-scoped knowledge search
- agent execution traces
- human approval gate for write actions

Docker CLI was not available on the local validation machine, so the container image build is intentionally left for Step 8 on a Docker-capable deployment environment.

Next: Step 8 — deploy the backend/frontend/database path, run public smoke tests, and verify the live demo.
