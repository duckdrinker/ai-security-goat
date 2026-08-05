import openai

client = openai.OpenAI()

SYSTEM_TEMPLATE = "You are a helpful assistant. User-submitted preferences: %s"


def read_user_preferences_from_request() -> str:
    """Stub — returns the raw, arbitrary-length preferences field submitted in the request body."""
    return "..."


def build_prompt(preferences: str) -> str:
    # Legacy %-formatting splices raw, unbounded user preferences into the system prompt with no length cap
    return SYSTEM_TEMPLATE % preferences


def recommend_product(question: str) -> str:
    system_prompt = build_prompt(read_user_preferences_from_request())
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question},
        ],
    )
    return response.choices[0].message.content
