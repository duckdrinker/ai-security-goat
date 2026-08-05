import json
import re
import smtplib
import sqlite3
from email.message import EmailMessage
import openai

client = openai.OpenAI()

ALLOWED_RECIPIENT_DOMAINS = {"acme.com"}


def validate_recipient(to: str) -> None:
    """Reject any recipient address outside the pre-approved domain allow-list before sending."""
    domain = to.split("@")[-1].lower()
    if domain not in ALLOWED_RECIPIENT_DOMAINS:
        raise ValueError(f"Recipient domain '{domain}' is not on the allow-list")


def send_email(to: str, subject: str, body: str) -> None:
    validate_recipient(to)
    msg = EmailMessage()
    msg["To"] = to
    msg["Subject"] = subject
    msg.set_content(body)
    with smtplib.SMTP("smtp.internal.acme.com") as server:
        server.send_message(msg)


response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Reply to the last customer email for me."}],
    tools=[{
        "type": "function",
        "function": {
            "name": "send_email",
            "description": "Send an email",
            "parameters": {"type": "object", "properties": {
                "to": {"type": "string"}, "subject": {"type": "string"}, "body": {"type": "string"},
            }},
        },
    }],
)
tool_call = response.choices[0].message.tool_calls[0]
args = json.loads(tool_call.function.arguments)
send_email(args["to"], args["subject"], args["body"])


db = sqlite3.connect("app.db")
ALLOWED_QUERY_PATTERN = re.compile(r"^SELECT \* FROM orders WHERE customer_id = \?$")


def execute_sql(customer_id: int):
    # Only a pre-approved, parameterized, read-only query shape is allowed — the LLM supplies the value, never the query structure
    query = "SELECT * FROM orders WHERE customer_id = ?"
    assert ALLOWED_QUERY_PATTERN.match(query)
    cursor = db.cursor()
    cursor.execute(query, (customer_id,))
    return cursor.fetchall()
