"""
Triggers llm-output-rendered-without-guardrail: the LLM's answer is spliced
into a Jinja2 template string and rendered server-side. Any HTML/JS the model
emits (e.g. because a document it summarized contained a prompt-injection
payload like "<script>...") is sent to the browser unsanitized — reflected/
stored XSS. render_template_string also re-opens SSTI risk if the response
text itself contains Jinja syntax.
"""
from flask import Flask, render_template_string, request
import openai

app = Flask(__name__)
client = openai.OpenAI()


@app.route("/summarize")
def summarize():
    doc_text = request.args.get("doc", "")
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Summarize the document for display on the support portal."},
            {"role": "user", "content": doc_text},
        ],
    )
    llm_response = completion.choices[0].message.content

    # llm_response is untrusted (it can echo attacker-controlled content from
    # doc_text) yet it's rendered as a live template with no escaping/sanitizing.
    return render_template_string(f"<div class='summary'>{llm_response}</div>")
