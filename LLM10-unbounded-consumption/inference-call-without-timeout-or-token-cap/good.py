"""
Mitigated equivalent: explicit token cap and request timeout on every
inference call. Does not trigger inference-call-without-timeout-or-token-cap.
"""
from __future__ import annotations

import os

from openai import OpenAI

CHAT_MODEL = "gpt-5.4"
MAX_TOKENS = 512
REQUEST_TIMEOUT_S = 30


def _client() -> OpenAI:
    # `timeout` bounds how long any single call can hang. Pair this with a
    # rate limiter (e.g. a token-bucket per API key/user) and a circuit
    # breaker upstream of this function, so repeated failures or timeouts
    # don't keep hammering the provider — and the wallet — indefinitely.
    return OpenAI(api_key=os.environ["OPENAI_API_KEY"], timeout=REQUEST_TIMEOUT_S)


def reply(user_msg: str) -> str:
    """Return the assistant reply for the given user message."""
    client = _client()
    response = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful support assistant."},
            {"role": "user", "content": user_msg},
        ],
        temperature=0.2,
        max_tokens=MAX_TOKENS,
        timeout=REQUEST_TIMEOUT_S,
    )
    return response.choices[0].message.content
