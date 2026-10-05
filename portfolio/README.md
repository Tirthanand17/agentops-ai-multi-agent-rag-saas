# Portfolio Media

This directory contains recruiter-facing evidence captured from the live AgentOps AI public demo.

## Final deliverables

- `agentops-ai-portfolio-demo.mp4`
  - 50.30 seconds
  - 1920x1080, 30 fps
  - H.264 video + AAC narration
  - 2.43 MB
  - built from real live-demo states and the verified architecture visual
- `agentops-narration.mp3`
  - English neural narration source used in the walkthrough
- `architecture/agentops-architecture.png`
  - recruiter-facing implemented-vs-future architecture visual
- `UPWORK_PORTFOLIO.md`
  - Upwork-ready title, role, description, skills, and media ordering
- `VIDEO_SCRIPT.md`
  - storyboard, narration, and truthfulness notes

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
- The video uses real live-demo captures; it is a polished portfolio walkthrough, not a claim of a continuous real-time screen recording.
