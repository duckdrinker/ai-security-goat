package demo;

import dev.langchain4j.model.chat.ChatModel;
import java.sql.Connection;
import java.sql.Statement;

public class Lookup {
    private final ChatModel model;
    private final Connection conn;

    public Lookup(ChatModel model, Connection conn) {
        this.model = model;
        this.conn = conn;
    }

    public void query(String question) throws Exception {
        String sql = model.chat("Write a SQL query for: " + question);
        try (Statement st = conn.createStatement()) {
            st.executeQuery(sql);
        }
    }
}