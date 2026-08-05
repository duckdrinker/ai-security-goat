"""
Triggers browsing-tool-raw-content-without-url-allowlist: a "deep research"
agent fetches a starting page, hands the extracted links to the LLM, and lets
it pick which link to follow next — recursively. Each hop re-uses the same
unguarded fetch, so a single malicious page (or a prompt-injected snippet
inside any fetched page) can redirect the crawl to internal/cloud-metadata
hosts several hops in, far from the original user-supplied URL.
"""
import re

import openai
import requests

client = openai.OpenAI()
LINK_RE = re.compile(r'href=["\'](https?://[^"\']+)["\']')


def _fetch(url: str) -> str:
    # Same unguarded fetch reused at every hop of the crawl.
    return requests.get(url, timeout=10).text


def deep_research(start_url: str, research_goal: str, max_hops: int = 5) -> list[str]:
    visited = []
    current_url = start_url

    for _ in range(max_hops):
        page_html = _fetch(current_url)
        visited.append(current_url)

        links = LINK_RE.findall(page_html)
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[{
                "role": "user",
                "content": f"Goal: {research_goal}\nLinks found: {links}\n"
                           f"Reply with ONLY the single best URL to follow next.",
            }],
        )
        next_url = completion.choices[0].message.content.strip()

        # The next hop is entirely LLM-chosen from page-supplied links, with
        # no allowlist gate before the next request is issued.
        current_url = next_url

    return visited
