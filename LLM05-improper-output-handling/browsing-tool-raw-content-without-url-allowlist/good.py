"""
Mitigated equivalent for browsing-tool-raw-content-without-url-allowlist.

Every URL — whether it comes from a user, from the LLM's own output, or from
a link extracted out of a previously-fetched page — is validated against an
explicit domain allowlist before any request is issued. The check also
resolves the hostname and rejects private/loopback/link-local IPs, and
redirects are validated the same way rather than followed blindly, so a
same-domain URL can't be used to redirect to an internal address.
"""
import ipaddress
import socket
from urllib.parse import urlparse

import requests

ALLOWED_DOMAINS = {"docs.python.org", "en.wikipedia.org", "www.nist.gov"}


def _is_public_ip(host: str) -> bool:
    try:
        addr = ipaddress.ip_address(socket.gethostbyname(host))
    except (socket.gaierror, ValueError):
        return False
    return not (
        addr.is_private or addr.is_loopback or addr.is_link_local or addr.is_reserved or addr.is_multicast
    )


def _is_allowed(url: str) -> bool:
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        return False
    if parsed.hostname not in ALLOWED_DOMAINS:
        return False
    return _is_public_ip(parsed.hostname)


def fetch_url(url: str) -> str:
    if not _is_allowed(url):
        raise ValueError(f"URL not permitted by allowlist: {url!r}")

    # Redirects are disabled and re-validated manually so a same-domain URL
    # can't 302 the request onward to a disallowed/internal host.
    response = requests.get(url, timeout=10, allow_redirects=False)
    while response.is_redirect:
        location = response.headers["Location"]
        if not _is_allowed(location):
            raise ValueError(f"Redirect target not permitted by allowlist: {location!r}")
        response = requests.get(location, timeout=10, allow_redirects=False)

    return response.text


def deep_research(start_url: str, research_goal: str, max_hops: int = 5) -> list[str]:
    """Even LLM-chosen follow-up links go back through the same allowlist gate."""
    import openai

    client = openai.OpenAI()
    visited = []
    current_url = start_url

    for _ in range(max_hops):
        if not _is_allowed(current_url):
            break
        page_html = fetch_url(current_url)
        visited.append(current_url)

        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": f"Goal: {research_goal}\nPage: {page_html[:2000]}\nReply with ONLY the next URL to follow, or 'DONE'."}],
        )
        next_url = completion.choices[0].message.content.strip()
        if next_url == "DONE" or not _is_allowed(next_url):
            break
        current_url = next_url

    return visited
