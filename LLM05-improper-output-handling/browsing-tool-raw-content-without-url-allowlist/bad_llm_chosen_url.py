"""
Triggers browsing-tool-raw-content-without-url-allowlist: the URL to fetch is
not even supplied by the end user — it's extracted straight out of the LLM's
own free-text response ("I should check this link: ...") and then fetched
immediately. This is the clearest form of the risk: the model itself, having
been influenced by earlier tool output or prompt injection, fully controls
where the next outbound request goes, with zero allowlisting.
"""
import re

import openai
import requests

client = openai.OpenAI()

URL_RE = re.compile(r"https?://\S+")


def research_agent_step(research_goal: str) -> str:
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[{
            "role": "user",
            "content": f"Research this topic: {research_goal}. "
                       f"Reply with a URL you want to fetch next to continue research.",
        }],
    )
    llm_response = completion.choices[0].message.content

    match = URL_RE.search(llm_response)
    if not match:
        return "No URL found."
    next_url = match.group(0)

    # The model chose this URL; nothing here restricts it to a known-safe
    # set of domains before the agent fetches it on the server's behalf.
    page = requests.get(next_url, timeout=10)
    return page.text
