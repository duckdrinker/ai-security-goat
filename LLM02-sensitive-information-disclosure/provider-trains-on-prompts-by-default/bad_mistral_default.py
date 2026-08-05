"""
Uses Mistral's La Plateforme API on the standard tier without enabling the
enterprise "no training on inputs" agreement, and without any per-request
opt-out. Triggers provider-trains-on-prompts-by-default.
"""
from mistralai import Mistral

client = Mistral(api_key="mistral-api-key")


def classify_ticket(body: str) -> str:
    response = client.chat.complete(
        model="mistral-large-latest",
        messages=[{"role": "user", "content": body}],
    )
    return response.choices[0].message.content
