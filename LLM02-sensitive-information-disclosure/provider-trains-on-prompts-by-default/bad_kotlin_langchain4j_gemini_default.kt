package demo

import dev.langchain4j.model.googleai.GoogleAiGeminiChatModel

fun model(): GoogleAiGeminiChatModel =
    GoogleAiGeminiChatModel.builder()
        .apiKey(System.getenv("GEMINI_API_KEY"))
        .modelName("gemini-2.0-flash")
        .build()