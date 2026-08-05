"""
Mitigated: same public Flask chat endpoint, but every message is checked
against a prompt-extraction guardrail before it ever reaches the LLM. Known
extraction patterns ("ignore previous instructions", "print/show/repeat your
system prompt", "what are your instructions", etc.) are blocked with a canned
refusal instead of being forwarded.
"""
import re

from flask import Flask, request, jsonify
from openai import OpenAI

app = Flask(__name__)
client = OpenAI()

SYSTEM_PROMPT = "You are Acme's public product-help chatbot. Be concise and friendly."

_EXTRACTION_PATTERNS = [
    r"ignore (all|the )?(previous|above) instructions",
    r"(print|show|repeat|reveal|output)\s+(your|the)\s+(system\s+)?prompt",
    r"what (is|are) your (system prompt|instructions)",
    r"repeat everything (above|before this)",
]
_EXTRACTION_RE = re.compile("|".join(_EXTRACTION_PATTERNS), re.IGNORECASE)


def looks_like_prompt_extraction(message: str) -> bool:
    return bool(_EXTRACTION_RE.search(message))


@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json["message"]

    if looks_like_prompt_extraction(user_message):
        return jsonify({"reply": "I can't share my internal configuration. How else can I help?"})

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
    )
    return jsonify({"reply": response.choices[0].message.content})
