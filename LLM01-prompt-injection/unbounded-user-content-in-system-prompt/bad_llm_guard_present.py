import openai
from llm_guard.input_scanners import PromptInjection

client = openai.OpenAI()
input_scanner = PromptInjection()


def chat(user_bio: str, question: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": f"You are a helpful assistant. Here is background info about the user: {user_bio}"},
            {"role": "user", "content": question},
        ],
    )
    return response.choices[0].message.content
