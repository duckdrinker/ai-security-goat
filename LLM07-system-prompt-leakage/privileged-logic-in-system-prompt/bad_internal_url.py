"""
Triggers privileged-logic-in-system-prompt: the prompt embeds an internal-only
admin endpoint. If the prompt leaks, the URL -- and the instruction that the
model can be told to call it -- leaks with it.
"""
import anthropic

client = anthropic.Anthropic()

SYSTEM_PROMPT = (
    "You are an internal IT helpdesk assistant. "
    "For password resets that require elevated privileges, call the admin "
    "API directly at https://internal-admin.corp.local/api/reset-password "
    "and follow the instructions it returns."
)


def handle_ticket(ticket_text: str) -> str:
    message = client.messages.create(
        model="claude-opus-4",
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": ticket_text}],
        max_tokens=500,
    )
    return message.content[0].text
