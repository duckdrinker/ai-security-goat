package demo;

public class Loop {
    private final Assistant assistant;

    public Loop(Assistant assistant) {
        this.assistant = assistant;
    }

    public void run() {
        String goal = "keep improving the report";
        for (int i = 0; i < 5; i++) {
            goal = assistant.chat(goal);
        }
    }
}