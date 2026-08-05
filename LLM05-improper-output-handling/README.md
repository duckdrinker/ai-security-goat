# LLM05: Improper Output Handling

This category covers cases where an application trusts an LLM's output and passes it on to a downstream interpreter — a shell, an `eval()`/`exec()` call, an HTML/Markdown renderer, or an outbound HTTP fetch triggered by an agent's browsing tool — without validating, sanitizing, or otherwise gating that output first. Because LLM output can itself be influenced by untrusted input (user prompts, retrieved documents, tool results, prompt injection), skipping that validation step turns the model into a conduit for remote code execution, cross-site scripting, or server-side request forgery against the systems that consume its answers.

| Detector | What it flags |
|---|---|
| `llm-output-to-shell-eval` | LLM output passed directly to `eval()`/`exec()` or a shell (`subprocess.run(..., shell=True)`, `os.system()`) with no validation — risk of remote code execution. |
| `llm-output-rendered-without-guardrail` | LLM output rendered as HTML/Markdown without sanitization (e.g. `render_template_string()`, `Markup()`, autoescape disabled) — risk of XSS. |
| `browsing-tool-raw-content-without-url-allowlist` | An agent's browsing/fetch tool requests an arbitrary URL (including one chosen by the LLM itself) with no domain allowlist — risk of SSRF. |
