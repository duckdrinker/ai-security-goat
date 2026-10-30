import org.springframework.ai.tool.annotation.Tool;

public class CleanTool {

    @Tool(description = "Adds two numbers and returns the sum.")
    public int add(int a, int b) {
        return a + b;
    }
}
