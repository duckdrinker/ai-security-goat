import google.generativeai as genai

model = genai.GenerativeModel("gemini-2.5-pro")


def describe_user_video(video_file_path: str, question: str) -> str:
    video_file = genai.upload_file(path=video_file_path)
    # User-uploaded video is uploaded and referenced directly with no content-safety screening before inference
    response = model.generate_content([video_file, question])
    return response.text
