# ASI03: Identity Abuse (Non-Human Identity)

OWASP Agentic Security Initiative category, not part of the LLM Top 10:2025 taxonomy — added 2026-08-31 (xygeni/xygeni-product-backlog#1358) as this collection's first non-LLM category. Covers identity/privilege abuse vectors specific to AI agents and the tools/servers they run: static long-lived credentials ripe for theft, credentials shared across agents without per-agent scoping (lateral movement once one agent is compromised), and MCP servers running with more privilege than they need (containment failure if compromised). Same folder/`expected.yaml` conventions as the `LLM0N-*` categories — see the top-level `ai-security-goat/README.md`.

| Detector | What it flags |
|---|---|
| [`agent-uses-static-long-lived-credential`](./agent-uses-static-long-lived-credential/) | An agent/tool manifest contains a hardcoded secret (API key, password, connection string) with no reference to a credential manager and no rotation/TTL metadata. |
| [`tool-credential-shared-across-agents`](./tool-credential-shared-across-agents/) | Two or more agents reference the same credential/connection without per-agent scope — if one agent is compromised, the attacker inherits every agent's access on that connection. |
| [`mcp-server-runs-as-privileged`](./mcp-server-runs-as-privileged/) | An MCP server's container/process manifest (Dockerfile, docker-compose, Kubernetes, systemd) has no privilege-restriction declaration, or explicitly runs as root. |
