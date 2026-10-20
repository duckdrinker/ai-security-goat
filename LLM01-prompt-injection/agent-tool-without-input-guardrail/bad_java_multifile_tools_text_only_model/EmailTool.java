package demo;

import dev.langchain4j.agent.tool.Tool;

public class EmailTool {
    @Tool("Sends an email to the given address")
    public String send(String to, String body) {
        return "sent to " + to;
    }
}