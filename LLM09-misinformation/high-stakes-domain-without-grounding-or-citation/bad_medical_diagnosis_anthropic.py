"""
Triggers high-stakes-domain-without-grounding-or-citation: a medical
diagnosis assistant answers straight from the model's parametric knowledge --
no lookup against a medical knowledge base, and no citation requirement in
the prompt.
"""
from anthropic import Anthropic

client = Anthropic()


def diagnose_symptoms(symptom_description: str) -> str:
    msg = client.messages.create(
        model="claude-3-5-sonnet-latest",
        max_tokens=500,
        system=(
            "You are a medical diagnosis assistant. Analyze the patient's "
            "symptoms and provide a likely diagnosis and treatment plan."
        ),
        messages=[{"role": "user", "content": symptom_description}],
    )
    return msg.content[0].text
