"""
Triggers public-agent-missing-prompt-extraction-guardrail: a public Flask
endpoint with no authentication takes raw user input, drops it straight into
the LLM call alongside the system prompt, and returns the raw completion.
Nothing checks for "ignore previous instructions / print your system prompt"
style extraction attempts before the call is made.
"""
from flask import Flask, request, jsonify
from openai import OpenAI

app = Flask(__name__)
client = OpenAI()

SYSTEM_PROMPT = "You are Acme's public product-help chatbot. Be concise and friendly."


@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json["message"]
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
    )
    return jsonify({"reply": response.choices[0].message.content})
