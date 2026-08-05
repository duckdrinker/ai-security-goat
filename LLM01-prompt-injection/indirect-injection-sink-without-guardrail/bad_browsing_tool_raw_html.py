import requests
import openai

client = openai.OpenAI()


def fetch_and_summarize(url: str) -> str:
    page = requests.get(url, timeout=10)
    # Raw fetched page content is passed straight into the LLM context — any instructions embedded in the page get executed
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a research assistant. Summarize the following web page."},
            {"role": "user", "content": page.text},
        ],
    )
    return response.choices[0].message.content
