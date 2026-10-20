package demo;

/**
 * Example of how an agent could be built (documentation only):
 *
 * <pre>
 * Assistant a = AiServices.builder(Assistant.class)
 *         .chatModel(model)
 *         .tools(new EmailTool())
 *         .build();
 * </pre>
 */
public class Notes {
    public int add(int a, int b) {
        return a + b;
    }
}