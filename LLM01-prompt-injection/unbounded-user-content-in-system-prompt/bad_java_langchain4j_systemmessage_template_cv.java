package _2_sequential_workflow;

import dev.langchain4j.agentic.Agent;
import dev.langchain4j.service.SystemMessage;
import dev.langchain4j.service.UserMessage;
import dev.langchain4j.service.V;

public interface CvTailor {

    @Agent("Tailors a CV according to specific instructions")
    @SystemMessage("""
            Here is a CV that needs tailoring to a specific job description, feedback or other instruction.
            You can drop irrelevant things if it makes the CV better suited to the instructions.
            The master CV: {{masterCv}}
            """)
    @UserMessage("""
            Here are the instructions for tailoring the CV: {{instructions}}
            """)
    String tailorCv(@V("masterCv") String masterCv, @V("instructions") String instructions);
}