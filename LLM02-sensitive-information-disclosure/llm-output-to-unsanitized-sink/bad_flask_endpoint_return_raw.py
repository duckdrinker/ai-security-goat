"""
A Flask chatbot endpoint returns the raw model completion straight to the HTTP
client with no sanitization. If the system prompt or retrieved context
contained internal notes or another user's PII, it is now exposed externally.
Triggers llm-output-to-unsanitized-sink.
"""
from flask import Flask, jsonify, request
from openai import OpenAI

app = Flask(__name__)
client = OpenAI()


def fetch_internal_account_notes(account_id: str) -> str:
    ...


@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json["message"]
    account_notes = fetch_internal_account_notes(request.json["account_id"])
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": f"Internal account notes: {account_notes}"},
            {"role": "user", "content": user_message},
        ],
    )
    return jsonify({"reply": response.choices[0].message.content})
