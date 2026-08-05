"""
Mitigates high-stakes-domain-without-grounding-or-citation: before answering a
legal question, the relevant statutes/case law are retrieved from a curated
knowledge base and passed to the model as grounding context, and the model is
instructed to cite them, instead of answering from parametric memory alone.
"""
import openai

client = openai.OpenAI()


def retrieve_relevant_statutes(user_question: str) -> list[str]:
    # Vector-search / lookup against a curated, vetted legal knowledge base.
    ...


def get_legal_advice(user_question: str) -> str:
    context_documents = retrieve_relevant_statutes(user_question)
    context_block = "\n\n".join(context_documents)

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": (
                "You are a legal information assistant. Answer ONLY using "
                "the source documents below, and cite the specific statute "
                "or case for every claim you make. If the sources do not "
                "cover the question, say so instead of guessing.\n\n"
                f"SOURCES:\n{context_block}"
            )},
            {"role": "user", "content": user_question},
        ],
    )
    return completion.choices[0].message.content
