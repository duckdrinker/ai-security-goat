package demo;

public class Loop {
    private final Assistant assistant;

    public Loop(Assistant assistant) {
        this.assistant = assistant;
    }

    public void run() {
        String goal = "keep improving the report";
        while (true) {
            goal = assistant.chat(goal);
        }
    }
}