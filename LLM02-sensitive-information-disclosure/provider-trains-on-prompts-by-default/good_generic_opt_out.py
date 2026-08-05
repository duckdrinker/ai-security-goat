"""
Mitigated: the in-house gateway is constructed with training_opt_out=True,
the provider-equivalent of an explicit "do not train on this data" flag.
"""


class LLMGateway:
    def __init__(self, api_key: str, training_opt_out: bool = False):
        self.api_key = api_key
        self.training_opt_out = training_opt_out

    def complete(self, prompt: str) -> str:
        raise NotImplementedError


gateway = LLMGateway(api_key="internal-gw-key", training_opt_out=True)
answer = gateway.complete("Draft a refund policy for order #48213, customer jane@example.com")
