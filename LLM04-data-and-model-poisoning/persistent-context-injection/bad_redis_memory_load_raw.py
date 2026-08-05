"""Agent memory persisted in Redis is loaded raw and replayed forever.

Triggers persistent-context-injection: on resume, the raw stored
conversation is loaded and appended to the live prompt with no check
that it hasn't been tampered with (e.g. by a prior injected "remember
this forever" instruction), and it is written straight back unchanged.
"""
import json

import redis
from openai import OpenAI

r = redis.Redis(host="localhost", port=6379)
client = OpenAI()


def resume_agent(user_id: str, new_message: str):
    raw = r.get(f"memory:{user_id}")
    history = json.loads(raw) if raw else []
    history.append({"role": "user", "content": new_message})
    reply = client.chat.completions.create(model="gpt-4o", messages=history)
    history.append({"role": "assistant", "content": reply.choices[0].message.content})
    r.set(f"memory:{user_id}", json.dumps(history))  # persists whatever was injected, forever
    return reply
