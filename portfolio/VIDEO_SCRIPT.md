# AgentOps AI — Final Portfolio Walkthrough

## Final render

- Duration: 50.30 seconds
- Resolution: 1920x1080
- Frame rate: 30 fps
- Video codec: H.264
- Audio: AAC narration
- File size: 2.43 MB
- Output: `agentops-ai-portfolio-demo.mp4`

## Scene order

1. Product hook
2. Grounded tenant-scoped RAG
3. Observable multi-agent execution trace
4. Human approval gate for a write action
5. Synthetic action completed after explicit approval
6. Architecture close with future production hardening separated

## Final narration

AgentOps AI is a full-stack operations demo combining grounded RAG, tool-using agents, and human approval for sensitive actions. Here, tenant-scoped knowledge search retrieves evidence with source names and similarity scores. The renewal-risk workflow then uses policy context and synthetic customer data, exposing every step in the execution trace. For write operations, the agent does not execute immediately. It pauses at a human approval gate, clearly labels the requested action, and waits. Only after approval does the synthetic ticket complete, preserving a visible audit trail. The live demo also reports seeded retrieval and routing evaluations, plus API health. It showcases practical RAG, agent orchestration, safety, and full-stack AI engineering.

## Editing / publishing guardrails

- Do not show browser bookmarks, email addresses, account identifiers, or unrelated tabs.
- Do not add third-party company logos.
- Keep on-screen text readable.
- Use only real deployed demo states and synthetic data.
- Do not claim production users, persistent PostgreSQL/pgvector, or production authentication/RBAC.
- Treat 100% evaluation numbers as seeded-fixture results only.
