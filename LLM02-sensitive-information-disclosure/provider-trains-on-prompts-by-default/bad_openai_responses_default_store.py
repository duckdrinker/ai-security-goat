"""
Calls OpenAI's Responses API without setting store=False. On the default
configuration, prompts/outputs are persisted and eligible for product
improvement use — no opt-out flag is configured anywhere in this code path.
Triggers provider-trains-on-prompts-by-default.
"""
from openai import OpenAI

client = OpenAI()


def ask_support_bot(question: str) -> str:
    response = client.responses.create(
        model="gpt-4o-mini",
        input=question,
    )
    return response.output_text


print(ask_support_bot("How do I reset my account password?"))
