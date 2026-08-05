"""
Triggers llm-output-rendered-without-guardrail: flask.Markup() (and its
successor markupsafe.Markup) explicitly tells Jinja2 "this string is already
safe HTML, do not autoescape it." Wrapping raw LLM output in Markup()
deliberately disables the one guardrail Flask gives you for free.
"""
from flask import Flask, Markup, render_template
import openai

app = Flask(__name__)
client = openai.OpenAI()


@app.route("/chat-reply")
def chat_reply():
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": "Answer the customer's question with rich formatting."}],
    )
    llm_response = completion.choices[0].message.content

    # Markup() bypasses Jinja2 autoescaping entirely — the template will
    # insert llm_response verbatim, including any <script>/onerror= payload.
    safe_looking_html = Markup(llm_response)
    return render_template("chat_reply.html", reply=safe_looking_html)
