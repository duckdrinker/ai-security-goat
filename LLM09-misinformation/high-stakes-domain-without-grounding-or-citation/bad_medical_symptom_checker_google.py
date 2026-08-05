"""
Triggers high-stakes-domain-without-grounding-or-citation: a Gemini-based
symptom checker performs medical diagnosis directly -- no RAG over a medical
corpus, and no system instruction to cite sources for the diagnosis.
"""
import google.generativeai as genai

genai.configure(api_key="...")

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    system_instruction=(
        "You are a medical diagnosis assistant. Given the patient's "
        "reported symptoms, provide a probable diagnosis and next steps."
    ),
)


def check_symptoms(symptom_description: str) -> str:
    response = model.generate_content(symptom_description)
    return response.text
