package demo

import dev.langchain4j.agent.tool.Tool
import dev.langchain4j.model.openai.OpenAiChatModel
import dev.langchain4j.service.AiServices
import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.RequestParam
import org.springframework.web.bind.annotation.RestController

interface Assistant {
    fun chat(message: String): String
}

class EmailTool {
    @Tool("Sends an email to the given address")
    fun send(to: String, body: String): String = "sent to $to"
}

@RestController
class SupportAgent {
    private val assistant: Assistant

    init {
        val model = OpenAiChatModel.builder()
            .apiKey(System.getenv("OPENAI_API_KEY"))
            .modelName("gpt-4o")
            .build()
        assistant = AiServices.builder(Assistant::class.java)
            .chatModel(model)
            .tools(EmailTool())
            .build()
    }

    @GetMapping("/chat")
    fun chat(@RequestParam q: String): String = assistant.chat(q)
}