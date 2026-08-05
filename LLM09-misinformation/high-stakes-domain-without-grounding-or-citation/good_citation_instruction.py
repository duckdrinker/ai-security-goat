"""
Mitigates high-stakes-domain-without-grounding-or-citation: without a full
retrieval pipeline, the medical assistant is instead explicitly instructed to
ground every claim in a named, citable clinical source, and to refuse to make
claims it cannot source -- rather than presenting unsourced diagnoses as fact.
"""
from anthropic import Anthropic

client = Anthropic()


def diagnose_symptoms(symptom_description: str) -> str:
    msg = client.messages.create(
        model="claude-3-5-sonnet-latest",
        max_tokens=500,
        system=(
            "You are a medical information assistant, not a doctor. For "
            "every possible condition you mention, cite the specific "
            "clinical guideline or peer-reviewed source it comes from. If "
            "you cannot cite a source for a claim, do not make the claim, "
            "and always recommend the user confirm with a licensed "
            "physician before acting on this information."
        ),
        messages=[{"role": "user", "content": symptom_description}],
    )
    return msg.content[0].text
