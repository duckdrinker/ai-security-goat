"""Loads a pickled conversation memory and reinjects it into the context.

Triggers persistent-context-injection: a previous session's persisted
memory blob is deserialized and appended straight to the new prompt
with no revalidation/sanitization of potentially attacker-controlled
persisted state (and pickle.load on untrusted data is itself unsafe).
"""
import pickle

from openai import OpenAI

client = OpenAI()


def resume_session(session_id: str):
    with open(f"sessions/{session_id}.pkl", "rb") as f:
        memory = pickle.load(f)  # untrusted persisted state, deserialized directly
    messages = memory["messages"] + [{"role": "user", "content": "Continue."}]
    return client.chat.completions.create(model="gpt-4o", messages=messages)
