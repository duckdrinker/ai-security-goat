package demo;

import dev.langchain4j.model.openai.OpenAiChatModel;

public class Config {
    public OpenAiChatModel model() {
        return OpenAiChatModel.builder()
                .apiKey(System.getenv("OPENAI_API_KEY"))
                .modelName("gpt-4o")
                .build();
    }
}