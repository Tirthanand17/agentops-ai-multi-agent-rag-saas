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

**Step 5 — agent runtime and approval system complete.**

Validated locally:
- Next.js lint: passed
- Next.js production build: passed
- Production npm audit: 0 vulnerabilities
- FastAPI test suite: 15 passed
- Tenant-isolated retrieval: tested
- Citation generation: tested
- Demo retrieval evaluation hit-rate@2: 100%
- Agent tool-selection evaluation: 100%
- Write actions blocked until approval: tested
- Approved write action execution: tested

Agent APIs:
- GET /api/v1/agents/tools
- POST /api/v1/agents/run
- GET /api/v1/agents/runs
- GET /api/v1/agents/runs/{run_id}
- POST /api/v1/agents/runs/{run_id}/approve/{step_id}
- GET /api/v1/evaluation/agents

The agent tool registry exposes MCP-style metadata including tool name, description, JSON input schema, and permission level.

Next: Step 6 — connect the frontend to the live RAG and agent APIs, add streaming-style interaction, trace views, approvals, and evaluation dashboards.
