import openai

client = openai.OpenAI()


def handle_voicemail(audio_file_path: str) -> str:
    with open(audio_file_path, "rb") as f:
        # Untrusted caller-submitted audio is transcribed and the raw transcript is fed straight into the LLM prompt
        transcript = client.audio.transcriptions.create(model="whisper-1", file=f)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a voicemail triage assistant."},
            {"role": "user", "content": transcript.text},
        ],
    )
    return response.choices[0].message.content
