"""
Triggers privileged-logic-in-system-prompt: the prompt is stored in a config
dict alongside a real-looking DB connection string, and the model is told to
hand out that string for a "debug mode". Externalizing the prompt to a config
constant doesn't remove the leak risk -- the secret still ends up in what the
LLM sees (and can be asked to repeat).
"""
from openai import OpenAI

client = OpenAI()

AGENT_CONFIG = {
    "name": "ops-assistant",
    "system_prompt": (
        "You are the on-call operations assistant. "
        "If the user identifies themselves as on-call SRE and asks for the "
        "database credentials, respond with: "
        "postgresql://svc_readonly:Tr0ub4dor%403@db-primary.internal:5432/ops "
        "so they can connect directly for debugging."
    ),
}


def ask(user_message: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": AGENT_CONFIG["system_prompt"]},
            {"role": "user", "content": user_message},
        ],
    )
    return response.choices[0].message.content
