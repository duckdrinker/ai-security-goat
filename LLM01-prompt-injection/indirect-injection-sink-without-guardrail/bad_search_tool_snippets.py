import anthropic
import requests

client = anthropic.Anthropic()


def web_search_tool(query: str) -> str:
    results = requests.get("https://api.example-search.com/search", params={"q": query}).json()
    # Raw search-result snippets from the open web are concatenated verbatim into the tool result content
    return "\n".join(r["snippet"] for r in results["results"])


tool_result = web_search_tool("Acme merger news")

followup = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "What's the latest news on the merger?"},
        {"role": "assistant", "content": [
            {"type": "tool_use", "id": "toolu_01", "name": "web_search", "input": {"query": "Acme merger"}},
        ]},
        {"role": "user", "content": [
            {"type": "tool_result", "tool_use_id": "toolu_01", "content": tool_result},
        ]},
    ],
)
