"""
Mitigated: explicitly sets store=False on the Responses API call so the
prompt and output are not retained/used beyond serving this single request.
"""
from openai import OpenAI

client = OpenAI()


def ask_support_bot(question: str) -> str:
    response = client.responses.create(
        model="gpt-4o-mini",
        input=question,
        store=False,
    )
    return response.output_text
