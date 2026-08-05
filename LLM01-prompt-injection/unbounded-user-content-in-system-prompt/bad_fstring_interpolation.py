import openai

client = openai.OpenAI()


def build_system_prompt(user_bio: str) -> str:
    # Raw user-controlled text spliced directly into the system prompt with no length cap or sanitization
    return f"You are a helpful assistant. Here is background info about the user: {user_bio}"


def chat(user_bio: str, question: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": build_system_prompt(user_bio)},
            {"role": "user", "content": question},
        ],
    )
    return response.choices[0].message.content
