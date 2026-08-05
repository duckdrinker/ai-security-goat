"""
Mitigated: the FastAPI endpoint redacts the completion before returning it to
the caller, so any PII echoed back by the model is scrubbed first.
"""
import re

from fastapi import FastAPI
from openai import OpenAI
from pydantic import BaseModel

app = FastAPI()
client = OpenAI()

EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")


def redact(text: str) -> str:
    return EMAIL_RE.sub("[EMAIL]", text)


class TicketRequest(BaseModel):
    ticket_id: str
    customer_history: str
    question: str


@app.post("/assist")
def assist(req: TicketRequest):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": f"Ticket history:\n{req.customer_history}"},
            {"role": "user", "content": req.question},
        ],
    )
    answer = response.choices[0].message.content
    return {"answer": redact(answer)}
