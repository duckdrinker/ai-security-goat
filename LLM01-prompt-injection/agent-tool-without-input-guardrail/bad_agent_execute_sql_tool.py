import json
import sqlite3
import openai

client = openai.OpenAI()
db = sqlite3.connect("app.db")


def execute_sql(query: str):
    # LLM-composed SQL string is executed directly against the production database — no parameterization,
    # no allow-list of statement shapes, no read-only restriction
    cursor = db.cursor()
    cursor.execute(query)
    return cursor.fetchall()


tools = [{
    "type": "function",
    "function": {
        "name": "execute_sql",
        "description": "Run a SQL query against the customer database",
        "parameters": {"type": "object", "properties": {"query": {"type": "string"}}},
    },
}]

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "How many orders did customer 4821 place last month?"}],
    tools=tools,
)
tool_call = response.choices[0].message.tool_calls[0]
args = json.loads(tool_call.function.arguments)
rows = execute_sql(args["query"])
