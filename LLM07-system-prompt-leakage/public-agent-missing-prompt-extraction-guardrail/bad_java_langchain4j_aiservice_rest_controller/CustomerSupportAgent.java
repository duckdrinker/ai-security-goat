package dev.langchain4j.example;

import dev.langchain4j.service.MemoryId;
import dev.langchain4j.service.Result;
import dev.langchain4j.service.SystemMessage;
import dev.langchain4j.service.UserMessage;
import dev.langchain4j.service.spring.AiService;

@AiService
public interface CustomerSupportAgent {

    @SystemMessage("""
            Your name is Roger, you are a customer support agent of a car rental company named 'Miles of Smiles'.
            You are friendly, polite and concise.
            Today is {{current_date}}.
            """)
    Result<String> answer(@MemoryId String memoryId, @UserMessage String userMessage);
}