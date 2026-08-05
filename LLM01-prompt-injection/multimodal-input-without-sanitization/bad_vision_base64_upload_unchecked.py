import base64
import anthropic

client = anthropic.Anthropic()


def analyze_uploaded_image(image_bytes: bytes, question: str) -> str:
    encoded = base64.standard_b64encode(image_bytes).decode("utf-8")
    # Raw user-uploaded image bytes are handed directly to the vision model — no moderation, no embedded-text/QR scan
    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": [
                {"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": encoded}},
                {"type": "text", "text": question},
            ],
        }],
    )
    return message.content
