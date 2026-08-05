"""
Mitigated (alternative approach): instead of a single regex, a lightweight
heuristic scores the request on several independent signals (explicit
"ignore instructions" phrasing, requests to repeat/reveal system content,
meta-questions about the assistant's own configuration) and blocks anything
over a threshold before the LLM is ever called.
"""
from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI

app = FastAPI()
client = OpenAI()

SYSTEM_PROMPT = "You are the public FAQ assistant for Acme's docs site."

_SUSPICIOUS_PHRASES = [
    "ignore previous instructions",
    "ignore the instructions above",
    "system prompt",
    "your instructions",
    "your rules",
    "verbatim",
    "repeat the text above",
    "disregard your guidelines",
]


def extraction_risk_score(message: str) -> int:
    lowered = message.lower()
    return sum(1 for phrase in _SUSPICIOUS_PHRASES if phrase in lowered)


class ChatRequest(BaseModel):
    message: str


@app.post("/api/public/chat")
async def chat(req: ChatRequest):
    if extraction_risk_score(req.message) >= 2:
        return {"reply": "I'm not able to discuss my internal configuration."}

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": req.message},
        ],
    )
    return {"reply": response.choices[0].message.content}
