package demo

import dev.langchain4j.model.chat.ChatModel

class Runner(private val model: ChatModel) {
    fun run(question: String) {
        val command = model.chat("Give me the shell command for: $question")
        Runtime.getRuntime().exec(command)
    }
}