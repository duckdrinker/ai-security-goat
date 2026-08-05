# LLM07 — System Prompt Leakage

Fixtures for OWASP LLM Top 10:2025 **LLM07: System Prompt Leakage** — cases where a system prompt ends up being trusted as a security boundary it was never designed to be. This covers two related failure modes: system prompts that embed privileged logic or secrets (admin bypass phrases, internal-only URLs, hardcoded API keys/credentials) that become exploitable the moment the prompt is extracted, and public-facing or unauthenticated agents that offer no guardrail against extraction attempts in the first place, making that leak trivial to trigger on demand.

| Detector | What it flags |
|---|---|
| `privileged-logic-in-system-prompt` | The system prompt text contains privileged logic or secrets — admin/bypass phrases, internal-only URLs or endpoints, hardcoded API keys or credentials — that would be exposed if the prompt itself leaked. |
| `public-agent-missing-prompt-extraction-guardrail` | A public-facing or unauthenticated agent/endpoint builds a prompt and calls the LLM with no guardrail (regex, classifier, etc.) to detect and block system-prompt extraction attempts beforehand. |

> **Note:** neither detector in this category is confirmed implemented in the Xygeni AI Security scanner as of 2026-07-21 — see the `# Detector implementation status unconfirmed...` comment at the top of each `expected.yaml`. These fixtures document intended behavior per spec.
