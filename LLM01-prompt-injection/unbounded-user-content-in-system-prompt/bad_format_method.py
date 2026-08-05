import openai

client = openai.OpenAI()

SYSTEM_TEMPLATE = "You are a helpful assistant for {company}. Customer profile: {profile}"


def get_user_profile_freetext() -> str:
    """Stub — returns arbitrary-length free-text profile data submitted by the end user."""
    return "..."


def build_prompt(company: str, profile: str) -> str:
    # .format() splices unsanitized, unbounded user profile data into the system prompt
    return SYSTEM_TEMPLATE.format(company=company, profile=profile)


def handle_order_question(question: str) -> str:
    system_prompt = build_prompt("Acme Corp", get_user_profile_freetext())
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question},
        ],
    )
    return response.choices[0].message.content
