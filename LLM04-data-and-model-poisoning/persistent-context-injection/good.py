"""Mitigated: persisted memory is revalidated before reinjection.

Entries are re-scanned for injected-instruction phrasing and truncated
before being folded back into a new session's context.
"""
import json
import re

INJECTION_MARKERS = re.compile(
    r"(ignore (all|previous) instructions|system prompt|you must now)", re.I
)


def revalidate_memory(entries: list[str]) -> list[str]:
    clean = []
    for entry in entries:
        if INJECTION_MARKERS.search(entry):
            continue  # drop suspicious persisted entries
        clean.append(entry[:500])
    return clean


def load_long_term_memory(user_id: str) -> str:
    with open(f"memory/{user_id}.json") as f:
        facts = json.load(f)["facts"]
    return "\n".join(revalidate_memory(facts))
