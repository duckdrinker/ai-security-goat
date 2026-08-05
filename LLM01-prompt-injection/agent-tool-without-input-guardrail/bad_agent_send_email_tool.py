import json
import smtplib
from email.message import EmailMessage
import openai

client = openai.OpenAI()


def send_email(to: str, subject: str, body: str) -> None:
    # LLM-generated recipient/subject/body executed as-is — no allow-list, no confirmation step, no content check
    msg = EmailMessage()
    msg["To"] = to
    msg["Subject"] = subject
    msg.set_content(body)
    with smtplib.SMTP("smtp.internal.acme.com") as server:
        server.send_message(msg)


tools = [{
    "type": "function",
    "function": {
        "name": "send_email",
        "description": "Send an email on behalf of the user",
        "parameters": {
            "type": "object",
            "properties": {
                "to": {"type": "string"},
                "subject": {"type": "string"},
                "body": {"type": "string"},
            },
        },
    },
}]

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Reply to the last customer email for me."}],
    tools=tools,
)
tool_call = response.choices[0].message.tool_calls[0]
args = json.loads(tool_call.function.arguments)
send_email(args["to"], args["subject"], args["body"])
