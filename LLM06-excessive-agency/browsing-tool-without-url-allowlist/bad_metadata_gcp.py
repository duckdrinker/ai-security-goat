"""
bad_metadata_gcp.py
Triggers browsing-tool-without-url-allowlist at Critical severity: a
function-calling-style browsing tool with no URL allowlist, invoked with the
GCP metadata endpoint to steal the service account's access token.
"""
import requests

TOOLS = {
    "fetch_url": {
        "description": "Fetch the raw text content of a web page given its URL.",
        "parameters": {"url": "string"},
    }
}


def fetch_url(url: str) -> str:
    response = requests.get(url, timeout=10)
    return response.text


def run_tool_call(tool_name: str, args: dict) -> str:
    if tool_name == "fetch_url":
        return fetch_url(args["url"])
    raise ValueError(f"Unknown tool: {tool_name}")


# Attacker-controlled agent step:
result = run_tool_call("fetch_url", {"url": "http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token"})
