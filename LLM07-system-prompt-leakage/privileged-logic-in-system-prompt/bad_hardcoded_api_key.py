"""
Triggers privileged-logic-in-system-prompt: a live-looking service API key is
pasted directly into the prompt text so the model can "use" it. Prompt
extraction now doubles as credential theft.
"""
from openai import OpenAI

client = OpenAI()

SYSTEM_PROMPT = """You are a data-lookup assistant.
When you need to query the internal reporting service to answer a question,
authenticate with this key: sk-internal-reporting-9f3a7c2b1e4d5f6a8b9c0d1e2f3a4b5c
Include it as the Authorization header value, prefixed with "Bearer "."""


def query(user_message: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
    )
    return response.choices[0].message.content
