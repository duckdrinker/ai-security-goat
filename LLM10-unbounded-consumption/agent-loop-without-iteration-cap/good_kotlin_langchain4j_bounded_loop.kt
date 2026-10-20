package demo

class Loop(private val assistant: Assistant) {
    fun run() {
        var goal = "keep improving the report"
        repeat(5) {
            goal = assistant.chat(goal)
        }
    }
}