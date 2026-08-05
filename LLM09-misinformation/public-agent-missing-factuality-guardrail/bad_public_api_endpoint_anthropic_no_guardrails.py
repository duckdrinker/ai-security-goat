"""
Triggers public-agent-missing-factuality-guardrail: this public REST
endpoint exposes the assistant to any anonymous caller (no auth) and returns
the raw Anthropic completion untouched -- there is no fact-checking,
citation, or grounding guardrail anywhere between the model and the HTTP
response.
"""
from anthropic import Anthropic
from flask import Flask, jsonify, request

app = Flask(__name__)
client = Anthropic()


@app.route("/public/ask", methods=["POST"])
def public_ask():
    user_question = request.json["question"]
    msg = client.messages.create(
        model="claude-3-5-sonnet-latest",
        max_tokens=500,
        system="You are Acme's public-facing help assistant, answering questions from anonymous website visitors.",
        messages=[{"role": "user", "content": user_question}],
    )
    return jsonify({"answer": msg.content[0].text})
