"""
Triggers browsing-tool-without-url-allowlist: the agent's browsing tool is
registered with no domain/allowlist parameter anywhere in its definition --
the model can pass literally any URL (internal metadata endpoints, internal
services, arbitrary external hosts) and the tool will fetch it.
"""
from langchain.tools import Tool
import requests


def browse_url(url: str) -> str:
    resp = requests.get(url, timeout=10)
    return resp.text[:5000]


browse_tool = Tool.from_function(
    func=browse_url,
    name="browse_url",
    description="Fetch the content of any URL the user or task refers to.",
)
