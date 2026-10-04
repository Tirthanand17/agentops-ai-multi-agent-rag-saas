# System Architecture

## Product boundaries

AgentOps AI is intentionally a portfolio-grade AI SaaS rather than a basic chatbot.

The application must prove:
1. modern full-stack web development
2. applied AI/ML and NLP
3. LLM/RAG and agent orchestration
4. production engineering and safety
5. deployment and observability

## Core services

### Web application
Responsibilities:
- authentication
- workspace switching
- knowledge-base management
- chat and agent-run UI
- execution traces
- analytics
- settings
- voice interaction controls

### FastAPI backend
Responsibilities:
- authenticated API surface
- tenant-aware data access
- document ingestion
- RAG retrieval
- agent execution
- tool routing
- SSE event streaming
- evaluation endpoints
- audit logging

### PostgreSQL / pgvector
Primary entities:
- users
- workspaces
- memberships
- documents
- chunks
- conversations
- messages
- agent_runs
- agent_steps
- tool_calls
- approvals
- eval_cases
- eval_results
- audit_events

## AI architecture

### RAG flow
1. upload document
2. extract text
3. normalize
4. chunk with metadata
5. embed
6. persist vectors
7. retrieve candidates
8. optional rerank
9. produce grounded answer
10. attach citations

### Agent runtime
Agent state includes:
- user request
- current plan
- retrieved context
- available tools
- tool results
- approval state
- final response
- trace metadata

Tool classes:
- read-only
- write/action
- external integration

Write/action tools require explicit approval in the public demo.

### MCP-style tool gateway
Each tool exposes:
- name
- description
- input schema
- execution function
- permission level
- timeout
- retry policy

## Demo business tools

Synthetic data only:
- search knowledge base
- lookup customer
- lookup order
- summarize account
- create support ticket
- draft follow-up email
- calculate KPI
- post demo webhook

## Security and reliability

- tenant ID required for business data queries
- no secrets in frontend
- environment-variable validation
- structured tool schemas
- write-tool approval gates
- prompt-injection-aware retrieval handling
- output validation
- request limits
- timeouts and retries
- audit trail for every agent action

## Evaluation

RAG:
- retrieval hit rate
- citation correctness
- groundedness heuristic
- answer relevance

Agent:
- tool-selection accuracy
- task completion
- invalid-tool rate
- approval bypass rate
- average step count
- latency

## Deployment target

Frontend: Vercel
Backend: Render or Railway-compatible container
Database: Supabase PostgreSQL + pgvector
CI: GitHub Actions

## Voice extension

Browser voice mode comes first.

Later telephony extension:
- Vapi / Retell / Twilio adapter
- call transfer
- appointment scheduling
- call summary
- CRM webhook
