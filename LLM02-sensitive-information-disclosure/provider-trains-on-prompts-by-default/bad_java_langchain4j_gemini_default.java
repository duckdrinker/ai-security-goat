package demo;

import dev.langchain4j.model.googleai.GoogleAiGeminiChatModel;

public class Config {
    public GoogleAiGeminiChatModel model() {
        return GoogleAiGeminiChatModel.builder()
                .apiKey(System.getenv("GEMINI_API_KEY"))
                .modelName("gemini-2.0-flash")
                .build();
    }
}