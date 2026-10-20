package demo;

import dev.langchain4j.agent.tool.Tool;
import dev.langchain4j.model.openai.OpenAiChatModel;
import dev.langchain4j.service.AiServices;

public class AutorunMailer {

    interface Operator {
        String run(String task);
    }

    static class MailTools {
        @Tool("Sends an email to any address")
        public String sendEmail(String to, String body) {
            return "sent to " + to;
        }
    }

    public static void main(String[] args) {
        OpenAiChatModel model = OpenAiChatModel.builder()
                .apiKey(System.getenv("OPENAI_API_KEY"))
                .modelName("gpt-4o")
                .build();
        Operator operator = AiServices.builder(Operator.class)
                .chatModel(model)
                .tools(new MailTools())
                .build();
        String task = "Triage the inbox and answer every customer.";
        while (true) {
            task = operator.run(task);
        }
    }
}