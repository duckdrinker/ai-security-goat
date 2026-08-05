"""
Persists the raw LLM response to a plaintext transcript file for "audit"
purposes, with no redaction. The transcript directory is broadly readable by
other services on the box. Triggers llm-output-to-unsanitized-sink.
"""
import anthropic

client = anthropic.Anthropic()


def answer_and_log(user_id: str, prompt: str) -> str:
    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=512,
        messages=[{"role": "user", "content": prompt}],
    )
    text = response.content[0].text
    with open(f"transcripts/{user_id}.txt", "a") as f:
        f.write(text + "\n")
    return text
