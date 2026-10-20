import dev.langchain4j.model.chat.ChatModel;
import dev.langchain4j.model.input.Prompt;
import dev.langchain4j.model.input.PromptTemplate;
import java.util.HashMap;
import java.util.Map;
import org.apache.jena.query.QueryExecution;
import org.apache.jena.query.QueryExecutionFactory;
import org.apache.jena.query.QueryFactory;
import org.apache.jena.query.ResultSetFormatter;

public class DbpediaAnswer {

    static String abstractOf(String subject) {
        String sparql = "SELECT ?abstract WHERE { <http://dbpedia.org/resource/" + subject
                + "> <http://dbpedia.org/ontology/abstract> ?abstract }";
        try (QueryExecution qexec = QueryExecutionFactory.sparqlService(
                "http://dbpedia.org/sparql", QueryFactory.create(sparql))) {
            return ResultSetFormatter.asText(qexec.execSelect());
        }
    }

    static String answer(ChatModel model, String question, String subject) {
        PromptTemplate template = PromptTemplate.from(
                "Answer the question using this text:\n{{text}}\n\nQuestion: {{question}}");
        Map<String, Object> variables = new HashMap<>();
        variables.put("text", abstractOf(subject));
        variables.put("question", question);
        Prompt prompt = template.apply(variables);
        return model.chat(prompt.text());
    }
}