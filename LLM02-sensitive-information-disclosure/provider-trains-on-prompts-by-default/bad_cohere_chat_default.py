"""
Sends chat prompts to Cohere's API using the default client configuration. No
opt-out / data-usage preference is set on the client or the request, so the
provider's default data-usage terms apply to every message sent through it.
Triggers provider-trains-on-prompts-by-default.
"""
import cohere

co = cohere.Client("co-api-key")


def draft_reply(customer_message: str) -> str:
    response = co.chat(message=customer_message, model="command-r-plus")
    return response.text
