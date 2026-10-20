package demo;

import dev.langchain4j.model.chat.ChatModel;

public class Runner {
    private final ChatModel model;

    public Runner(ChatModel model) {
        this.model = model;
    }

    public void run(String question) throws Exception {
        String command = model.chat("Give me the shell command for: " + question);
        Runtime.getRuntime().exec(command);
    }
}