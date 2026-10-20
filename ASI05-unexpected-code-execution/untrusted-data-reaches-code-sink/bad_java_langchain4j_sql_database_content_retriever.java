package _3_advanced;

import dev.langchain4j.experimental.rag.content.retriever.sql.SqlDatabaseContentRetriever;
import dev.langchain4j.model.chat.ChatModel;
import dev.langchain4j.model.openai.OpenAiChatModel;
import dev.langchain4j.rag.content.retriever.ContentRetriever;
import dev.langchain4j.service.AiServices;
import javax.sql.DataSource;

public class SqlRag {

    interface Assistant {
        String chat(String message);
    }

    public static void main(String[] args) {
        DataSource dataSource = createDataSource();
        ChatModel model = OpenAiChatModel.builder()
                .apiKey(System.getenv("OPENAI_API_KEY"))
                .modelName("gpt-4o-mini")
                .build();
        ContentRetriever retriever = SqlDatabaseContentRetriever.builder()
                .dataSource(dataSource)
                .chatModel(model)
                .build();
        Assistant assistant = AiServices.builder(Assistant.class)
                .chatModel(model)
                .contentRetriever(retriever)
                .build();
        System.out.println(assistant.chat("How many customers placed an order last month?"));
    }

    private static DataSource createDataSource() {
        return null;
    }
}