package demo;

import dev.langchain4j.agent.tool.Tool;
import dev.langchain4j.model.openai.OpenAiChatModel;
import dev.langchain4j.service.AiServices;
import java.util.Scanner;

public class ApprovedMailer {

    interface Operator {
        String run(String task);
    }

    static class MailTools {
        private final Scanner in = new Scanner(System.in);

        @Tool("Sends an email after a human approves it")
        public String sendEmail(String to, String body) {
            System.out.println("Approve email to " + to + "? [y/N]");
            if (!"y".equalsIgnoreCase(in.nextLine().trim())) {
                return "denied by the operator";
            }
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
        System.out.println(operator.run("Draft a reply to the customer."));
    }
}