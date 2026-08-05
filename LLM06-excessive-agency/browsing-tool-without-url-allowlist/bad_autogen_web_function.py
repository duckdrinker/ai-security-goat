"""
Triggers browsing-tool-without-url-allowlist: an AutoGen function tool for
fetching web pages is registered against the assistant with a completely open
`url: str` parameter -- no allowlist, no domain check, no scheme restriction.
"""
import autogen
import urllib.request


def fetch_webpage(url: str) -> str:
    with urllib.request.urlopen(url, timeout=10) as resp:
        return resp.read().decode("utf-8", errors="ignore")[:5000]


assistant = autogen.AssistantAgent(name="researcher", llm_config={"model": "gpt-4o"})
user_proxy = autogen.UserProxyAgent(name="user_proxy", human_input_mode="NEVER", code_execution_config=False)

autogen.register_function(
    fetch_webpage,
    caller=assistant,
    executor=user_proxy,
    name="fetch_webpage",
    description="Fetch the raw HTML of any URL for research purposes.",
)
