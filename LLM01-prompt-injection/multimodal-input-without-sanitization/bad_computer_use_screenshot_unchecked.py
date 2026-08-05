import base64
import anthropic

client = anthropic.Anthropic()


def analyze_screen(screenshot_bytes: bytes) -> str:
    encoded = base64.standard_b64encode(screenshot_bytes).decode("utf-8")
    # Live screenshot of a third-party web page is sent directly to the model — any on-screen text
    # (including hidden or off-screen injected instructions) is processed unfiltered
    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1024,
        tools=[{"type": "computer_20250124", "name": "computer", "display_width_px": 1280, "display_height_px": 800}],
        messages=[{
            "role": "user",
            "content": [
                {"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": encoded}},
                {"type": "text", "text": "What should I click next?"},
            ],
        }],
    )
    return message.content
