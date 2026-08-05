"""
Triggers high-stakes-domain-without-grounding-or-citation: the system prompt
explicitly frames this as legal advice, but the model is called directly with
no retrieval step and no instruction to cite sources -- whatever the model
hallucinates is handed back as authoritative legal guidance.
"""
import openai

client = openai.OpenAI()


def get_legal_advice(user_question: str) -> str:
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": (
                "You are a legal advisor. Provide clear legal advice to help "
                "the user understand their rights and obligations."
            )},
            {"role": "user", "content": user_question},
        ],
    )
    return completion.choices[0].message.content
