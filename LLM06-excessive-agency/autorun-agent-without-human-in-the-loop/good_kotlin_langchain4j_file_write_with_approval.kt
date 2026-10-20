package demo

import dev.langchain4j.agent.tool.Tool
import dev.langchain4j.model.openai.OpenAiChatModel
import dev.langchain4j.service.AiServices
import java.io.File

interface Operator {
    fun run(task: String): String
}

class FileTools {
    @Tool("Writes a file after a human approves it")
    fun writeFile(path: String, content: String): String {
        println("Approve write to $path? [y/N]")
        if (readLine()?.trim()?.lowercase() != "y") return "denied by the operator"
        File(path).writeText(content)
        return "written $path"
    }
}

fun main() {
    val model = OpenAiChatModel.builder()
        .apiKey(System.getenv("OPENAI_API_KEY"))
        .modelName("gpt-4o")
        .build()
    val operator = AiServices.builder(Operator::class.java)
        .chatModel(model)
        .tools(FileTools())
        .build()
    println(operator.run("Update the README."))
}