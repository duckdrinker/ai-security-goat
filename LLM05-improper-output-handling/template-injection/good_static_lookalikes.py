"""
Mitigated: none of these strings ever reach a template-rendering sink
(Template(), env.from_string(), render_template_string(), Handlebars.compile(),
ejs.render()) -- they only look like template syntax.
"""


def call_llm(prompt: str) -> str:
    ...  # returns raw, untrusted model output


# Generic English words that happen to include "template"/"render" -- not a
# call to any template engine.
status_message = call_llm("Describe the current render pipeline state in plain English")
print(status_message)

# A ${...} interpolation, but this is a plain shell-style config string being
# written to a .env file, never passed to Mako's Template().
db_url_pattern = "postgres://${DB_USER}:${DB_PASS}@${DB_HOST}/app"
with open("config/db.env.template", "w") as f:
    f.write(db_url_pattern)

# A Python .format() placeholder -- .format() is not a template-injection
# sink, it's a plain string method.
report = "Ticket #{id}: {summary}".format(id=42, summary=call_llm("Summarize the ticket"))
