"""
In-house gateway wrapper around a third-party hosted LLM. The gateway exposes
a training_opt_out flag that defaults to False, and callers never override it,
so every prompt sent through this client — including ones containing customer
PII — is eligible for provider-side training. Triggers
provider-trains-on-prompts-by-default.
"""


class LLMGateway:
    def __init__(self, api_key: str, training_opt_out: bool = False):
        self.api_key = api_key
        self.training_opt_out = training_opt_out  # never set to True below

    def complete(self, prompt: str) -> str:
        # ... sends `prompt` and `self.training_opt_out` to the provider's HTTP API ...
        raise NotImplementedError


gateway = LLMGateway(api_key="internal-gw-key")
answer = gateway.complete("Draft a refund policy for order #48213, customer jane@example.com")
