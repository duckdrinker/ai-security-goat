"""Entity memory is persisted to disk and reloaded verbatim next run.

Triggers persistent-context-injection: entity facts learned (and
potentially injected) in a previous, possibly compromised session are
loaded from disk and merged back into the live entity store with no
re-check before the next run uses them as context.
"""
import json

from langchain.memory import ConversationEntityMemory
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o")
memory = ConversationEntityMemory(llm=llm)


def reload_entity_memory(path: str = "entity_store.json"):
    with open(path) as f:
        stored = json.load(f)
    memory.entity_store.store.update(stored)  # reinjected as-is, no revalidation
    return memory


def save_entity_memory(path: str = "entity_store.json"):
    with open(path, "w") as f:
        json.dump(memory.entity_store.store, f)
