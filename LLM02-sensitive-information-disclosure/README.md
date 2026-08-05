# LLM02: Sensitive Information Disclosure

This category covers code paths where sensitive data — PII/PHI destined for training data, prompts, or model context — ends up somewhere it shouldn't: sent to an external model/provider without anonymization, retained by a provider that trains on prompts by default with no opt-out configured in code, or echoed back out through an LLM response into an unsanitized log, file, or HTTP sink. (A related sub-case — a secret hardcoded directly into a prompt string — is intentionally out of scope here: it's already covered by Xygeni's existing Secrets scanner, not a new AI Security detector.)

| Detector | What it flags | Fixtures |
|---|---|---|
| [`pii-dataset-to-external-model`](pii-dataset-to-external-model/) | A dataset containing PII/PHI is used for fine-tuning, or sent to an external model/provider (chat prompt, embeddings), without an anonymization/redaction step first. | 5 bad, 2 good |
| [`provider-trains-on-prompts-by-default`](provider-trains-on-prompts-by-default/) | Code calls an LLM provider that trains on submitted prompts by default, with no explicit opt-out (e.g. `store=False` or the provider's equivalent) configured. | 5 bad, 2 good |
| [`llm-output-to-unsanitized-sink`](llm-output-to-unsanitized-sink/) | The LLM's response — which may carry sensitive data leaked from its own context — is sent to a log, file, or HTTP response without redaction/sanitization first. | 5 bad, 2 good |

> As of 2026-07-21, none of these three detectors are confirmed implemented in the Xygeni AI Security scanner — each `expected.yaml` documents intended behavior per spec rather than an observed finding.
