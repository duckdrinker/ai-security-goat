"""
Triggers browsing-tool-without-url-allowlist: a CrewAI research agent is given
a scraping tool with no allowed_domains/allowlist configuration -- the agent
is registered generically as a "web researcher" and can direct the scraper at
any host the model decides is worth visiting.
"""
from crewai import Agent
from crewai.tools import BaseTool
import httpx


class ScrapePageTool(BaseTool):
    name: str = "scrape_page"
    description: str = "Scrape the text content of any web page."

    def _run(self, url: str) -> str:
        return httpx.get(url, follow_redirects=True).text


researcher = Agent(
    role="Web Researcher",
    goal="Gather background information from the web for the report",
    backstory="You browse the open web to find supporting sources.",
    tools=[ScrapePageTool()],
)
