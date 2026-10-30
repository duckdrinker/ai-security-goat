from openai import OpenAI

client = OpenAI()

SYSTEM_PROMPT = """You are a financial advisor. Recommend which stocks and securities to buy and how to allocate the investment portfolio."""


def ask(question: str) -> str:
    resp = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": question},
        ],
        max_tokens=256,
        timeout=30,
    )
    return resp.choices[0].message.content
