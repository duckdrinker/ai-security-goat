"""
Prints the full LLM response to stdout for debugging. If the model's context
included sensitive data pulled from a customer record, it lands unfiltered in
console output / captured logs. Triggers llm-output-to-unsanitized-sink.
"""
from openai import OpenAI

client = OpenAI()


def handle_support_query(customer_context: str, question: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": f"Customer record: {customer_context}"},
            {"role": "user", "content": question},
        ],
    )
    answer = response.choices[0].message.content
    print(answer)  # raw model output, unredacted
    return answer
