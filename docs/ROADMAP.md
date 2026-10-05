# Build Roadmap

## Phase 0 — Foundation
- monorepo scaffold
- frontend and backend package setup
- lint/test commands
- CI
- environment templates
- Docker development baseline

## Phase 1 — SaaS shell
- Next.js dashboard
- responsive navigation
- demo authentication flow
- workspace model
- seeded synthetic business data

## Phase 2 — Knowledge base / RAG
- document upload
- parsing
- chunking
- embeddings abstraction
- vector storage
- retrieval
- citations
- evaluation fixtures

## Phase 3 — Agent runtime
- state machine
- planner
- tool registry
- structured tool schemas
- tool execution
- trace logging
- approval gates

## Phase 4 — Business tools
- customer lookup
- order lookup
- ticket creation
- KPI calculator
- follow-up draft
- webhook tool
- synthetic demo dataset

## Phase 5 — Advanced UI
- streaming chat
- agent timeline
- source/citation viewer
- knowledge-base manager
- approval UI
- analytics dashboard

## Phase 6 — Evaluation & observability
- retrieval metrics
- agent metrics
- trace viewer
- latency/error metrics
- regression test suite

## Phase 7 — Voice
Status: completed 2026-10-05
- [x] browser speech-to-text
- [x] browser text-to-speech
- [x] voice controls
- [x] graceful fallback
- [x] baseline security headers and request-size limits
- [x] readiness endpoint and deployment documentation

## Phase 8 — Deployment
Status: completed 2026-10-05
- [x] choose zero-cost public-demo topology
- [x] add Render Blueprint
- [x] validate Next.js static export
- [x] define static-site security headers
- [x] complete pre-public secret-pattern scan
- [x] document stateless synthetic-demo behavior
- [x] create free Render backend service in Singapore
- [x] create free Render static frontend
- [x] restrict backend CORS to the deployed frontend origin
- [x] verify actual HTTPS service URLs
- [x] run live health, RAG, agent, and approval smoke tests
- [x] record public demo URL

Live frontend: https://agentops-ai-demo-tirthanand17.onrender.com
Live API: https://agentops-ai-api-tirthanand17.onrender.com

Persistent PostgreSQL/pgvector and real auth/RBAC are a production-hardening milestone and will only be marked complete after they are actually wired into runtime behavior.

## Phase 9 — Portfolio packaging
Status: in progress
- [x] polished 4:3 live screenshots
- [x] Upwork portfolio title/role/description draft
- [x] sub-60-second demo storyboard and narration script
- [x] recruiter-friendly architecture visual
- [x] 50-second 1080p portfolio walkthrough
- [x] natural English narration embedded in MP4
- [ ] final Upwork portfolio publishing
