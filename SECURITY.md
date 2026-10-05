# Security Policy for Demo

- Use synthetic data only.
- Never commit API keys or credentials.
- No destructive external actions in the public demo.
- Write actions require an explicit approval step.
- Do not expose tenant data across workspaces.
- Record agent actions and tool calls in an audit log.
- Validate structured model/tool output before execution.
- Bound public request sizes before agent or retrieval processing.
- Return baseline browser security headers from both frontend and backend.
- Browser microphone access is user-initiated and must fail safely when unsupported or denied.
- Keep the public portfolio deployment in demo mode unless real provider credentials are deliberately configured.
