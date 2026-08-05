"""
Triggers public-agent-missing-prompt-extraction-guardrail: a Streamlit app
deployed with no login/auth (the common default) pipes whatever the visitor
types directly to the model, with the system prompt attached and no guardrail
in between.
"""
import streamlit as st
from openai import OpenAI

client = OpenAI()

SYSTEM_PROMPT = """You are Acme's internal pricing-strategy assistant.
You know our full cost structure, margins, and upcoming price changes.
Only discuss this with people on the pricing team."""

user_input = st.text_input("Ask the pricing assistant:")

if user_input:
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_input},
        ],
    )
    st.write(response.choices[0].message.content)
