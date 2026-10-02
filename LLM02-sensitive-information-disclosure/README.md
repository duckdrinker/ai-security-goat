# LLM02: Sensitive Information Disclosure

This category covers code paths where sensitive data — PII/PHI destined for training data, prompts, or model context — ends up somewhere it shouldn't: sent to an external model/provider without anonymization, retained by a provider that trains on prompts by default with no opt-out configured in code, or echoed back out through an LLM response into an unsanitized log, file, or HTTP sink. (A related sub-case — a secret hardcoded directly into a prompt string — is intentionally out of scope here: it's already covered by Xygeni's existing Secrets scanner, not a new AI Security detector.)

| Detector | What it flags | Fixtures |
|---|---|---|
| [`pii-dataset-into-external-model`](pii-dataset-into-external-model/) | A dataset classified PII/PCI/PHI (shared sensitivity vocabulary, same as API Security) flows to an external model whose endpoint trains on prompts, or whose provider region is outside a configured data-residency boundary. | 9 bad, 4 good |
| [`provider-trains-on-prompts-by-default`](provider-trains-on-prompts-by-default/) | Code calls an LLM provider that trains on submitted prompts by default, with no explicit opt-out (e.g. `store=False` or the provider's equivalent) configured. | 5 bad, 2 good |
| [`llm-output-to-unsanitized-sink`](llm-output-to-unsanitized-sink/) | The LLM's response — which may carry sensitive data leaked from its own context — is sent to a log, file, or HTTP response without redaction/sanitization first. | 5 bad, 2 good |

> As of 2026-07-21, none of these three detectors were confirmed implemented in the Xygeni AI Security scanner. **Update 2026-10-02:** `pii-dataset-into-external-model` is confirmed implemented and dev-validated against a compiled build (xygeni/DepsDoctor#4496, PII/PCI/PHI harmonization — not merged yet as of this date); its `expected.yaml` reflects the confirmed behavior. The other two detectors are still unconfirmed.
