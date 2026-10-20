import dev.langchain4j.model.chat.ChatModel;
import org.apache.jena.query.QueryExecution;
import org.apache.jena.query.QueryExecutionFactory;
import org.apache.jena.query.QueryFactory;
import org.apache.jena.query.ResultSetFormatter;

public class DbpediaSubject {

    private final ChatModel model;

    public DbpediaSubject(ChatModel model) {
        this.model = model;
    }

    public String lookup(String question) {
        String subject = model.chat("Extract the subject of this question: " + question);
        String sparql = "SELECT ?abstract WHERE { <http://dbpedia.org/resource/" + subject
                + "> <http://dbpedia.org/ontology/abstract> ?abstract }";
        try (QueryExecution qexec = QueryExecutionFactory.sparqlService(
                "http://dbpedia.org/sparql", QueryFactory.create(sparql))) {
            return ResultSetFormatter.asText(qexec.execSelect());
        }
    }
}