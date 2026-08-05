import openai

client = openai.OpenAI()


def analyze_user_photo(image_url: str, question: str) -> str:
    # User-supplied image URL passed straight to the vision model with no content-safety check or provenance validation
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{
            "role": "user",
            "content": [
                {"type": "text", "text": question},
                {"type": "image_url", "image_url": {"url": image_url}},
            ],
        }],
    )
    return response.choices[0].message.content
