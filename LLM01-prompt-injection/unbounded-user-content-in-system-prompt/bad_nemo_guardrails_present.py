import openai
from nemoguardrails import LLMRails, RailsConfig

client = openai.OpenAI()
rails_config = RailsConfig.from_path("./guardrails_config")
rails = LLMRails(rails_config)


def chat(user_bio: str, question: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": f"You are a helpful assistant. Here is background info about the user: {user_bio}"},
            {"role": "user", "content": question},
        ],
    )
    return response.choices[0].message.content
