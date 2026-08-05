"""
Triggers browsing-tool-raw-content-without-url-allowlist: the agent's
"browse the web" tool takes whatever URL string it's given and fetches it
with requests.get(), with no check on scheme, host, or IP range. Since the
LLM decides the tool call arguments (including this URL) based on untrusted
page/user content, this is a direct SSRF primitive — it can be pointed at
http://169.254.169.254/latest/meta-data/ or an internal admin panel.
"""
import requests

TOOLS = {
    "fetch_url": {
        "description": "Fetch the raw text content of a web page given its URL.",
        "parameters": {"url": "string"},
    }
}


def fetch_url(url: str) -> str:
    # No scheme check, no domain allowlist, no protection against internal/
    # link-local addresses — url is whatever the agent loop passed through.
    response = requests.get(url, timeout=10)
    return response.text


def run_tool_call(tool_name: str, args: dict) -> str:
    if tool_name == "fetch_url":
        return fetch_url(args["url"])
    raise ValueError(f"Unknown tool: {tool_name}")
