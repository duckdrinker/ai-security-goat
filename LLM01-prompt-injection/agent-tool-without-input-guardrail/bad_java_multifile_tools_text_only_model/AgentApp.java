package demo;

import dev.langchain4j.model.openai.OpenAiChatModel;
import dev.langchain4j.service.AiServices;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class AgentApp {

    private final Assistant assistant;

    public AgentApp() {
        OpenAiChatModel model = OpenAiChatModel.builder()
                .apiKey(System.getenv("OPENAI_API_KEY"))
                .modelName("gpt-3.5-turbo")
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