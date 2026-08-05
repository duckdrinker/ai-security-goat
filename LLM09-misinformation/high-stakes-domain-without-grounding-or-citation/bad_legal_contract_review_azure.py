"""
Triggers high-stakes-domain-without-grounding-or-citation: contract review is
legal advice, but the Azure OpenAI deployment is called directly on the raw
contract text -- no clause/case-law database lookup, and no instruction to
cite sources for the flagged risks.
"""
from openai import AzureOpenAI

client = AzureOpenAI(
    api_version="2024-06-01",
    azure_endpoint="https://example-legal.openai.azure.com/",
)


def review_contract_clause(contract_text: str) -> str:
    completion = client.chat.completions.create(
        model="gpt-4o-legal-deployment",
        messages=[
            {"role": "system", "content": (
                "You provide legal advice on contract clauses, flagging "
                "risks and suggesting alternative legal wording."
            )},
            {"role": "user", "content": contract_text},
        ],
    )
    return completion.choices[0].message.content
