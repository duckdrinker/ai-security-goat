"""
A FastAPI support-ticket assistant returns the raw completion in the response
body. The prompt included the customer's full ticket history (with PII); the
model's response is echoed back unfiltered to whoever calls this endpoint.
Triggers llm-output-to-unsanitized-sink.
"""
from fastapi import FastAPI
from openai import OpenAI
from pydantic import BaseModel

app = FastAPI()
client = OpenAI()


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
    return {"answer": response.choices[0].message.content}
