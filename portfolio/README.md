# Portfolio Media

This directory contains recruiter-facing evidence captured from the live AgentOps AI public demo.

## Recommended image order

1. `screenshots/01-live-rag-dashboard.png`
   - Live tenant-scoped knowledge retrieval
   - 3 indexed synthetic sources
   - seeded RAG hit-rate@2 at 100%
   - seeded agent-routing accuracy at 100%
   - FastAPI backend online

2. `screenshots/02-live-agent-trace.png`
   - Multi-agent renewal-risk workflow
   - grounded knowledge-search step
   - synthetic customer lookup step
   - visible execution trace and completed result

3. `screenshots/03-live-approval-gate.png`
   - write action is blocked before execution
   - explicit human approval is required
   - trace clearly distinguishes READ and WRITE permissions

4. `screenshots/04-live-approved-action.png`
   - synthetic ticket action completes only after approval
   - completed write trace remains visible

All screenshots are 1400x1050 (4:3), captured from the deployed HTTPS application with synthetic demo data.

## Truthfulness notes

- No client data is shown.
- No real external ticket is created.
- `created-demo` actions are synthetic.
- 100% evaluation figures are results on the seeded demo fixture, not claims about real-world production accuracy.
- PostgreSQL/pgvector persistence and production authentication/RBAC remain future hardening work and are not presented as implemented.
