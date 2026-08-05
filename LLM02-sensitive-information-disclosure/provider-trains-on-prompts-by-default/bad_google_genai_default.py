"""
Uses the Google Generative AI SDK with a standard API key and no data-
governance configuration. On this tier, prompts remain eligible for use in
improving the provider's products unless the caller switches to an
enterprise/paid data-usage agreement — this code never does. Triggers
provider-trains-on-prompts-by-default.
"""
import google.generativeai as genai

genai.configure(api_key="AIzaSy-EXAMPLE-KEY")
model = genai.GenerativeModel("gemini-1.5-flash")


def summarize(document: str) -> str:
    response = model.generate_content(f"Summarize this contract:\n\n{document}")
    return response.text
