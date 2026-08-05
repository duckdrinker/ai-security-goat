"""
Mitigated equivalents for llm-output-rendered-without-guardrail.

The LLM's answer is always treated as untrusted user content: it goes through
an HTML sanitizer (bleach) with a strict allowlist of tags/attributes before
it is ever inserted into a page, and templates keep Jinja2's default
autoescaping enabled rather than opting out of it.
"""
import bleach
import markdown
from flask import Flask, render_template, Response
from jinja2 import Environment
import openai

app = Flask(__name__)
client = openai.OpenAI()

ALLOWED_TAGS = ["p", "b", "i", "em", "strong", "ul", "ol", "li", "code", "pre", "br", "a"]
ALLOWED_ATTRS = {"a": ["href", "title", "rel"]}


def sanitize(raw_html: str) -> str:
    return bleach.clean(raw_html, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRS, strip=True)


@app.route("/summarize")
def summarize():
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": "Summarize the document for display on the support portal."}],
    )
    llm_response = completion.choices[0].message.content

    # Flask's default Jinja env keeps autoescape=True for .html templates,
    # AND the content is sanitized before it's even passed in — defense in depth.
    return render_template("summary.html", summary=sanitize(llm_response))


@app.route("/notes/<note_id>")
def render_note(note_id):
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": f"Write a nicely formatted Markdown summary for note {note_id}."}],
    )
    llm_response = completion.choices[0].message.content

    raw_html = markdown.markdown(llm_response)
    return Response(sanitize(raw_html), mimetype="text/html")


# If a standalone Environment is genuinely needed, autoescape stays on and
# content is still sanitized before rendering.
safe_env = Environment(autoescape=True)
REPORT_TEMPLATE = safe_env.from_string("""
<section class="ai-report">
  <h2>AI-generated risk report</h2>
  <div>{{ body }}</div>
</section>
""")


def build_report_html(findings_summary: str) -> str:
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": f"Write an HTML-formatted risk report body for: {findings_summary}"}],
    )
    llm_response = completion.choices[0].message.content
    return REPORT_TEMPLATE.render(body=sanitize(llm_response))
