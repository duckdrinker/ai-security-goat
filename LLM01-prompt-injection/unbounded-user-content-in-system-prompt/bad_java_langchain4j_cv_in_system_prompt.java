package demo;

import dev.langchain4j.data.message.SystemMessage;
import dev.langchain4j.model.chat.ChatModel;

public class Screening {
    private final ChatModel model;

    public Screening(ChatModel model) {
        this.model = model;
    }

    public String screen(String candidateCv) {
        String system = "You are a recruiter. Evaluate this candidate. CV: " + candidateCv;
        return model.chat(SystemMessage.from(system).text());
    }
}