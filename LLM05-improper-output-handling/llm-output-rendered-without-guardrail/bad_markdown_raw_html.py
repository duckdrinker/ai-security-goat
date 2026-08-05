"""
Triggers llm-output-rendered-without-guardrail: the response is treated as
"just Markdown", converted with a renderer that passes raw inline HTML
through unchanged, and the resulting HTML is sent to the browser as-is. Since
Markdown allows literal HTML tags, this is XSS with a Markdown-shaped detour —
the model only has to emit `<img src=x onerror=alert(1)>` inside its answer.
"""
import markdown
from flask import Flask, Response
import openai

app = Flask(__name__)
client = openai.OpenAI()


@app.route("/notes/<note_id>")
def render_note(note_id):
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": f"Write a nicely formatted Markdown summary for note {note_id}."}],
    )
    llm_response = completion.choices[0].message.content

    # markdown.markdown() passes through raw HTML by default; no sanitizer
    # (bleach, nh3, etc.) is applied to the output before serving it.
    html = markdown.markdown(llm_response)
    return Response(html, mimetype="text/html")
