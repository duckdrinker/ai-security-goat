from openai import OpenAI

client = OpenAI()

SYSTEM_PROMPT = """You are an assistant that recommends securities, bonds and equities to buy for retirement savings."""


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
