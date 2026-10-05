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

Current demo data/platform:
- seeded synthetic business data
- tenant-scoped in-memory RAG/vector store
- workspace isolation tests
- in-memory agent execution traces
- no real client data or external write integrations

Production target:
- authentication and tenant-aware RBAC
- PostgreSQL + pgvector persistence
- durable audit/event log
- optional Redis-compatible cache/queue

Delivery:
- Dockerfiles and Docker Compose for local/container deployment
- GitHub Actions CI definition
- Render Blueprint for a free static Next.js demo + FastAPI service
- environment templates and deployment smoke-test checklist

## Current demo architecture

Browser / Next.js static frontend
 -> same-origin Render proxy routes
 -> FastAPI
    -> demo workspace isolation
    -> RAG pipeline + in-memory vector store
    -> agent runtime + structured tools
    -> human approval gates
    -> evaluation / execution traces

Production persistence/authentication are deliberately documented as the next hardening layer rather than claimed as already implemented.

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

**Step 8 — zero-cost Render deployment configuration validated; live service creation pending.**

Deployment preparation completed:
- root `render.yaml` defines a free FastAPI web service in Singapore and a free static Next.js site
- static frontend uses same-origin proxy rewrites to the backend
- static-site security headers are defined at the Render edge
- public demo remains synthetic/stateless; no unused database is provisioned just for a technology claim
- Git history pre-public scan found no obvious API-token/private-key patterns

Validated locally:
- FastAPI test suite: 17 passed
- focused frontend ESLint: passed
- Next.js Render/static-export build: passed
- `frontend/out/index.html`: generated
- Render YAML: parsed successfully with two services
- existing production npm audit result: 0 vulnerabilities

Integrated capabilities include:
- grounded tenant-scoped knowledge search
- RAG evaluation at 100% on the seeded fixture
- agent routing evaluation at 100% on the seeded fixture
- structured tool execution traces
- human approval gates for write actions
- browser speech input and response speech output

Next: create the two Render services, capture the actual live URLs, run the public smoke-test checklist, and then package screenshots/video for Upwork.
