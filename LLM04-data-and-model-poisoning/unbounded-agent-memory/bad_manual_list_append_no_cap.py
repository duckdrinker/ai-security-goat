"""Hand-rolled chat history is a plain list that only ever grows.

Triggers unbounded-agent-memory: every turn is appended and the full
list is sent to the model each time, with no truncation, summarization,
or cap anywhere in the code.
"""
from openai import OpenAI

client = OpenAI()
history: list[dict] = []


def chat(message: str):
    history.append({"role": "user", "content": message})
    reply = client.chat.completions.create(model="gpt-4o", messages=history)
    history.append({"role": "assistant", "content": reply.choices[0].message.content})
    return reply  # `history` has no max length anywhere
