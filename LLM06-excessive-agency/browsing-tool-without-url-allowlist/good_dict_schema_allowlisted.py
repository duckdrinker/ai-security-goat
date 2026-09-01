"""
Mitigated: same function-calling-style tool shape as the bad_* fixtures in
this folder, but fetch_url checks the hostname against an explicit allowlist
of trusted reference domains before making the request -- metadata/internal
addresses are rejected before any network call happens.
"""
from urllib.parse import urlparse

import requests

TOOLS = {
    "fetch_url": {
        "description": "Fetch the content of a URL from a fixed set of trusted reference sites.",
        "parameters": {"url": "string"},
    }
}

ALLOWED_DOMAINS = {"docs.python.org", "en.wikipedia.org", "arxiv.org"}


def fetch_url(url: str) -> str:
    host = urlparse(url).hostname or ""
    if host not in ALLOWED_DOMAINS:
        return f"Blocked: {host!r} is not in the allowlist {sorted(ALLOWED_DOMAINS)}."
    response = requests.get(url, timeout=10)
    return response.text


def run_tool_call(tool_name: str, args: dict) -> str:
    if tool_name == "fetch_url":
        return fetch_url(args["url"])
    raise ValueError(f"Unknown tool: {tool_name}")


result = run_tool_call("fetch_url", {"url": "https://docs.python.org/3/library/ipaddress.html"})
