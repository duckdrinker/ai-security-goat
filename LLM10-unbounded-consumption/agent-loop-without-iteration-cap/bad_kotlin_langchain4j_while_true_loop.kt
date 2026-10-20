package demo

class Loop(private val assistant: Assistant) {
    fun run() {
        var goal = "keep improving the report"
        while (true) {
            goal = assistant.chat(goal)
        }
    }
}