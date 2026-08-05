"""
Triggers browsing-tool-raw-content-without-url-allowlist: same missing
allowlist, different stack — an async agent tool built on httpx, used inside
a function-calling loop where the model supplies `url` as a JSON tool-call
argument. Async/httpx doesn't change the risk: no host/IP validation happens
before the request goes out.
"""
import httpx


async def fetch_page_tool(tool_call_args: dict) -> str:
    url = tool_call_args["url"]  # supplied verbatim by the LLM's function call

    async with httpx.AsyncClient(follow_redirects=True, timeout=10) as client:
        # No allowlist check on the host, no rejection of file://, no block
        # on RFC1918/link-local ranges before issuing the request.
        response = await client.get(url)
        return response.text
