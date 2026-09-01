"""
bad_metadata_allowlist_incomplete.py
Triggers browsing-tool-without-url-allowlist at Critical severity even
though an allowlist check IS present: it is scoped to "internal" IP ranges
(intended for reaching internal services) and was never narrowed to exclude
169.254.0.0/16 (link-local, includes cloud IMDS), so it still lets the tool
reach the cloud metadata/credential endpoint. An allowlist that fails to
exclude the credential store is not a real guardrail.
"""
import ipaddress
from urllib.parse import urlparse

import requests

TOOLS = {
    "fetch_url": {
        "description": "Fetch the raw text content of an internal-network URL.",
        "parameters": {"url": "string"},
    }
}

# Meant to scope requests to the company's internal network -- but
# 169.254.0.0/16 (link-local, includes cloud IMDS) was never excluded.
ALLOWED_RANGES = [
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("169.254.0.0/16"),
]


def fetch_url(url: str) -> str:
    host = urlparse(url).hostname or ""
    try:
        addr = ipaddress.ip_address(host)
    except ValueError:
        raise PermissionError(f"{host!r} is not an IP in the internal allowlist.")
    if not any(addr in net for net in ALLOWED_RANGES):
        raise PermissionError(f"{host!r} is outside the internal allowlist.")
    response = requests.get(url, timeout=10)
    return response.text


def run_tool_call(tool_name: str, args: dict) -> str:
    if tool_name == "fetch_url":
        return fetch_url(args["url"])
    raise ValueError(f"Unknown tool: {tool_name}")


# Attacker-controlled agent step -- passes the allowlist check above:
result = run_tool_call("fetch_url", {"url": "http://169.254.169.254/latest/meta-data/iam/security-credentials/"})
