"""Long-term memory JSON file is concatenated into the system prompt.

Triggers persistent-context-injection: content injected into memory in
a past session (e.g. via a crafted document the agent summarized) is
loaded from disk and replayed as trusted context in every new session,
with no filtering of what was written into the file.
"""
import json

from openai import OpenAI

client = OpenAI()


def load_long_term_memory(user_id: str) -> str:
    with open(f"memory/{user_id}.json") as f:
        facts = json.load(f)["facts"]
    return "\n".join(facts)  # no filtering of what was written into this file


def chat(user_id: str, message: str):
    memory_text = load_long_term_memory(user_id)
    system_prompt = f"You are an assistant. Known facts about the user:\n{memory_text}"
    return client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message},
        ],
    )
