import email
import openai

client = openai.OpenAI()


def summarize_inbox_message(raw_message: bytes) -> str:
    msg = email.message_from_bytes(raw_message)
    body = msg.get_payload(decode=True).decode(errors="ignore")
    # Untrusted email body — fully attacker-controlled by whoever sends the email — goes straight into the LLM prompt
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an email assistant. Draft a reply to this email."},
            {"role": "user", "content": body},
        ],
    )
    return response.choices[0].message.content
