"""
bad_dict_schema_generic.py
Triggers browsing-tool-without-url-allowlist at Critical severity: a
function-calling-style tool schema (TOOLS dict + matching function + call
dispatcher) exposes a fetch_url tool with no URL allowlist. This is the
framework-agnostic shape the detector actually recognizes -- LangChain/
CrewAI/AutoGen tool wrappers were tried first and did not trigger it (see
ER notes for AISC-100).
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
