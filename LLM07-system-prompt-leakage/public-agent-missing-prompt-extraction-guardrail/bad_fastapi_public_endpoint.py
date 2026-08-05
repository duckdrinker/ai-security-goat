"""
Triggers public-agent-missing-prompt-extraction-guardrail: a FastAPI endpoint
with no auth dependency and no request filtering -- any anonymous caller can
send arbitrary text, including prompt-extraction payloads, straight to the
model.
"""
from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI

app = FastAPI()
client = OpenAI()

SYSTEM_PROMPT = "You are the public FAQ assistant for Acme's docs site."


class ChatRequest(BaseModel):
    message: str


@app.post("/api/public/chat")
async def chat(req: ChatRequest):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": req.message},
        ],
    )
    return {"reply": response.choices[0].message.content}
