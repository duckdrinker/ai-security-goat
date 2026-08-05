from flask import Flask, request
from jinja2 import Template
import openai

app = Flask(__name__)
client = openai.OpenAI()

SYSTEM_TEMPLATE = Template("You are a helpful assistant. User bio: {{ user_bio }}")


@app.route("/chat", methods=["POST"])
def chat():
    user_bio = request.form["bio"]  # raw, unbounded, unsanitized request body field
    # Jinja2 autoescape targets HTML output, not prompt injection — it does not sanitize instruction-like text
    system_prompt = SYSTEM_TEMPLATE.render(user_bio=user_bio)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": "Hi"},
        ],
    )
    return response.choices[0].message.content
