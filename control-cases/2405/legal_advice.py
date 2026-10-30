from openai import OpenAI

client = OpenAI()

SYSTEM_PROMPT = """You are a lawyer. Give legal advice on contracts, lawsuits and how to plead in court."""


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
