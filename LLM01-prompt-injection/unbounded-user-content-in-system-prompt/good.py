import openai
import anthropic

openai_client = openai.OpenAI()
anthropic_client = anthropic.Anthropic()

MAX_USER_BIO_CHARS = 500
MAX_TICKET_NOTES_CHARS = 300


def sanitize_input(text: str, max_len: int = MAX_USER_BIO_CHARS) -> str:
    """Strip instruction-like control phrases and enforce a hard length cap before interpolation."""
    cleaned = text.replace("ignore previous instructions", "").replace("system prompt", "")
    return cleaned[:max_len]


def build_system_prompt(user_bio: str) -> str:
    safe_bio = sanitize_input(user_bio)
    return f"You are a helpful assistant. Here is background info about the user: {safe_bio}"


def chat(user_bio: str, question: str) -> str:
    response = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": build_system_prompt(user_bio)},
            {"role": "user", "content": question},
        ],
    )
    return response.choices[0].message.content


def fetch_ticket_notes_from_db(ticket_id: int) -> str:
    """Stub — queries the ticketing DB and returns free-text notes of arbitrary length."""
    return "..."


def build_ticket_system_prompt(ticket_notes: str) -> str:
    # Hard length cap bounds how much unsanitized user content can reach the system prompt
    bounded_notes = ticket_notes[:MAX_TICKET_NOTES_CHARS]
    return "You are an internal support agent. Additional context from the ticket: " + bounded_notes


def summarize_ticket(ticket_id: int) -> str:
    system_prompt = build_ticket_system_prompt(fetch_ticket_notes_from_db(ticket_id))
    message = anthropic_client.messages.create(
        model="claude-opus-4-6",
        system=system_prompt,
        max_tokens=512,
        messages=[{"role": "user", "content": "Summarize this ticket."}],
    )
    return message.content
