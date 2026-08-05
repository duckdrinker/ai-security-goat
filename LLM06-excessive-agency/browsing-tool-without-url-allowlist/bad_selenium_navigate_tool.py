"""
Triggers browsing-tool-without-url-allowlist: a browser-automation tool wraps
Selenium and calls driver.get(url) with whatever the model provides, so the
agent's headless browser can be pointed at any address it decides to visit --
no allowlist of permitted destinations is ever consulted.
"""
from langchain.tools import Tool
from selenium import webdriver

driver = webdriver.Chrome()


def navigate_and_read(url: str) -> str:
    driver.get(url)
    return driver.page_source[:5000]


navigate_tool = Tool.from_function(
    func=navigate_and_read,
    name="navigate_browser",
    description="Navigate a real browser to a URL and return the rendered page text.",
)
