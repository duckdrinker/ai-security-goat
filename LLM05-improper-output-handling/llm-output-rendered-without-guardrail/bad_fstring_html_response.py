"""
Triggers llm-output-rendered-without-guardrail: this is the backend
equivalent of `element.innerHTML = llmResponse` on a frontend — the handler
builds the HTTP response body itself by splicing the LLM's answer straight
into an HTML string, with no template engine (and therefore no escaping) at
all in the path.
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import urllib.request

API_KEY = "sk-..."


def ask_llm(question: str) -> str:
    body = json.dumps({
        "model": "gpt-4o",
        "messages": [{"role": "user", "content": question}],
    }).encode()
    req = urllib.request.Request(
        "https://api.openai.com/v1/chat/completions",
        data=body,
        headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req) as resp:
        return json.load(resp)["choices"][0]["message"]["content"]


class FAQHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        question = self.path.split("?q=", 1)[-1]
        llm_response = ask_llm(question)

        # Hand-built HTML with the raw LLM answer concatenated in directly —
        # no escaping, no sanitizer, no templating guardrail whatsoever.
        html = f"<html><body><p>You asked: {question}</p><p>Answer: {llm_response}</p></body></html>"

        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(html.encode())


if __name__ == "__main__":
    HTTPServer(("0.0.0.0", 8080), FAQHandler).serve_forever()
