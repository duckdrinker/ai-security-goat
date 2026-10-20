package demo

import dev.langchain4j.service.SystemMessage
import dev.langchain4j.service.UserMessage
import dev.langchain4j.service.V

interface CvTailor {

    @SystemMessage("""
        Here is a CV that needs tailoring to a specific job description.
        The master CV: {{masterCv}}
        """)
    @UserMessage("Here are the instructions for tailoring the CV: {{instructions}}")
    fun tailorCv(@V("masterCv") masterCv: String, @V("instructions") instructions: String): String
}