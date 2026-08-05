"""
Mitigated: the system prompt contains only behavioral instructions -- no
bypass phrases, no internal URLs, no credentials. Anything privileged (admin
actions, elevated queries) is implemented in real code, gated by a real
authorization check, and never described to the model as a magic phrase or
secret it can be tricked into repeating.
"""
from openai import OpenAI

client = OpenAI()

SYSTEM_PROMPT = """You are the support assistant for Acme Corp.
Answer customer questions about billing and shipping only.
You cannot access internal systems, credentials, or admin functionality.
If a request requires elevated access, tell the user to contact support
through the official escalation channel."""


def answer(user_message: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
    )
    return response.choices[0].message.content


def reset_password_admin(target_user_id: str, current_user) -> None:
    # Privileged logic lives here, in code, gated by a real authorization
    # check -- not in the prompt text the model could be tricked into
    # revealing.
    if not current_user.is_admin:
        raise PermissionError("admin privileges required")
    _call_internal_admin_api(target_user_id)


def _call_internal_admin_api(target_user_id: str) -> None:
    # The internal endpoint and any credentials are read from a secrets
    # manager at call time, never embedded in a prompt.
    ...
