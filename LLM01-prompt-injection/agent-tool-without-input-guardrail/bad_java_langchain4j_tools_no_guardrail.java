package demo;

import dev.langchain4j.agent.tool.Tool;
import dev.langchain4j.model.openai.OpenAiChatModel;
import dev.langchain4j.service.AiServices;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class SupportAgent {

    interface Assistant {
        String chat(String message);
    }

    static class EmailTool {
        @Tool("Sends an email to the given address")
        public String send(String to, String body) {
            return "sent to " + to;
        }
    }

    private final Assistant assistant;

    public SupportAgent() {
        OpenAiChatModel model = OpenAiChatModel.builder()
                .apiKey(System.getenv("OPENAI_API_KEY"))
                .modelName("gpt-4o")
                .build();
        this.assistant = AiServices.builder(Assistant.class)
                .chatModel(model)
                .tools(new EmailTool())
                .build();
    }

    @GetMapping("/chat")
    public String chat(@RequestParam String q) {
        return assistant.chat(q);
    }
}