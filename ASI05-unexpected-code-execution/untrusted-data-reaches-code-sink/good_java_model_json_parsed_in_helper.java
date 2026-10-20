package demo;

import com.fasterxml.jackson.databind.ObjectMapper;
import dev.langchain4j.model.chat.ChatModel;
import java.util.Map;

public class Parser {
    private final ChatModel model;
    private final ObjectMapper mapper = new ObjectMapper();

    public Parser(ChatModel model) {
        this.model = model;
    }

    private Map<String, Object> toMap(String json) throws Exception {
        return mapper.readValue(json, Map.class);
    }

    public Map<String, Object> extract(String text) throws Exception {
        String json = model.chat("Extract fields as JSON from: " + text);
        return toMap(json);
    }
}