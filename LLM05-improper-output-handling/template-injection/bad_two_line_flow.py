"""
bad_two_line_flow.py
Triggers template-injection: a network fetch's response is assigned to a
variable, then used two lines later to build a Jinja2 template string --
the taint still reaches the sink even though the flow spans a couple of
statements rather than a single expression.
"""
import requests
from jinja2 import Template

resp = requests.get("https://partner-api.example.com/announcement")
remote_text = resp.text

banner_template = f"Announcement: {remote_text}"
template = Template(banner_template)
output = template.render()
