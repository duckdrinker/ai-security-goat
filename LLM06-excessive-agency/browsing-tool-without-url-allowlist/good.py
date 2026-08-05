"""
Mitigated: the browsing tool takes a URL argument but checks its hostname
against an explicit allowlist before fetching anything. Requests to hosts
outside the allowlist (including internal/metadata addresses) are rejected
before the network call is made.
"""
from urllib.parse import urlparse

from langchain.tools import Tool
import requests

ALLOWED_DOMAINS = {"docs.python.org", "en.wikipedia.org", "arxiv.org"}


def browse_url(url: str) -> str:
    host = urlparse(url).hostname or ""
    if host not in ALLOWED_DOMAINS:
        return f"Blocked: {host!r} is not in the allowlist {sorted(ALLOWED_DOMAINS)}."
    resp = requests.get(url, timeout=10)
    return resp.text[:5000]


browse_tool = Tool.from_function(
    func=browse_url,
    name="browse_url",
    description="Fetch the content of a URL from a fixed set of trusted reference sites.",
)
