import anthropic

client = anthropic.Anthropic()


def fetch_ticket_notes_from_db(ticket_id: int) -> str:
    """Stub — in production this queries the ticketing DB and returns free-text notes of arbitrary length."""
    return "..."


def build_system_prompt(ticket_notes: str) -> str:
    base = "You are an internal support agent. Additional context from the ticket: "
    # Unbounded concatenation of arbitrary-length, unsanitized user-submitted ticket notes
    return base + ticket_notes


def summarize_ticket(ticket_id: int) -> str:
    system_prompt = build_system_prompt(fetch_ticket_notes_from_db(ticket_id))
    message = client.messages.create(
        model="claude-opus-4-6",
        system=system_prompt,
        max_tokens=512,
        messages=[{"role": "user", "content": "Summarize this ticket."}],
    )
    return message.content
