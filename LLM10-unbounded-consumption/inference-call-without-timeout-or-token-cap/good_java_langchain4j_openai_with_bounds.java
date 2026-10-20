package demo;

import dev.langchain4j.model.openai.OpenAiChatModel;
import java.time.Duration;

public class Config {
    public OpenAiChatModel model() {
        return OpenAiChatModel.builder()
                .apiKey(System.getenv("OPENAI_API_KEY"))
                .modelName("gpt-4o")
                .timeout(Duration.ofSeconds(30))
                .maxTokens(256)
                .build();
    }
}