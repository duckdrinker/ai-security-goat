package _7_supervisor_orchestration;

import dev.langchain4j.agentic.AgenticServices;
import dev.langchain4j.agentic.supervisor.SupervisorAgent;
import dev.langchain4j.model.chat.ChatModel;
import dev.langchain4j.model.openai.OpenAiChatModel;

public class SupervisorEmail {

    static class OrganizingTools {
        @dev.langchain4j.agent.tool.Tool("Sends an email to the given address")
        public String sendEmail(String to, String subject, String body) {
            return "sent to " + to;
        }
    }

    interface EmailAssistant {
        @dev.langchain4j.agentic.Agent("Sends emails to candidates")
        String send(String request);
    }

    public static void main(String[] args) {
        ChatModel model = OpenAiChatModel.builder()
                .apiKey(System.getenv("OPENAI_API_KEY"))
                .modelName("gpt-4o-mini")
                .build();

        EmailAssistant emailAssistant = AgenticServices.agentBuilder(EmailAssistant.class)
                .chatModel(model)
                .tools(new OrganizingTools())
                .build();

        SupervisorAgent hiringSupervisor = AgenticServices.supervisorBuilder()
                .chatModel(model)
                .subAgents(emailAssistant)
                .build();

        hiringSupervisor.invoke("Review the candidates and email each of them with the outcome.");
    }
}