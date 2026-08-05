"""
Triggers inference-call-without-timeout-or-token-cap: the Anthropic Messages
API requires a `max_tokens` argument, so this wrapper "satisfies" it with a
constant that is high enough to never actually bound anything (1,000,000
tokens), and never sets a request timeout or any retry/circuit-breaker
limit. A single pathological prompt (e.g. a jailbreak that asks for an
extremely long answer, or a document that confuses the model into repeating
itself) can run for minutes and bill for the full window before anything
stops it.
"""
from __future__ import annotations

import anthropic

_DEFAULT_MAX_TOKENS = 1_000_000  # "cap" in name only

client = anthropic.Anthropic()


def summarize(document: str) -> str:
    response = client.messages.create(
        model="claude-3-7-sonnet-latest",
        max_tokens=_DEFAULT_MAX_TOKENS,
        messages=[{"role": "user", "content": f"Summarize this document:\n\n{document}"}],
    )
    return response.content[0].text
