"""
Triggers browsing-tool-raw-content-without-url-allowlist: a LangChain-style
custom Tool exposes browsing to a ReAct agent. The agent framework parses the
LLM's "Action Input: <url>" text and calls `_run(url)` directly — the tool
implementation trusts that input completely and performs the fetch with no
domain/scheme validation.
"""
from langchain.tools import BaseTool
import requests


class WebBrowserTool(BaseTool):
    name: str = "browse_web"
    description: str = "Fetches the content of a given URL for the agent to read."

    def _run(self, url: str) -> str:
        # `url` is the "Action Input" the LLM produced in its ReAct trace —
        # it is executed as a live outbound HTTP request with no allowlist,
        # no scheme restriction, and no block on internal/loopback ranges.
        resp = requests.get(url, timeout=10, allow_redirects=True)
        return resp.text[:5000]

    async def _arun(self, url: str) -> str:
        return self._run(url)
