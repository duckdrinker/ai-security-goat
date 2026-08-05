"""
Triggers public-agent-missing-prompt-extraction-guardrail: a bare WebSocket
server accepting connections from any client, streaming every incoming
message straight into the LLM call. No auth handshake, no per-message
filtering for extraction attempts.
"""
import asyncio

import websockets
from openai import OpenAI

client = OpenAI()

SYSTEM_PROMPT = "You are Acme's live support agent. Help visitors with account questions."


async def handle_connection(websocket):
    async for user_message in websocket:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message},
            ],
        )
        await websocket.send(response.choices[0].message.content)


async def main():
    async with websockets.serve(handle_connection, "0.0.0.0", 8765):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
