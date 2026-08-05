"""
Triggers inference-call-without-timeout-or-token-cap: LangChain's ChatOpenAI
is instantiated with no `max_tokens` and no `request_timeout` / `timeout`,
and the chain has no retry/circuit-breaker wrapper around it. The
convenience wrapper hides the fact that the underlying OpenAI call is
exactly as unbounded as calling the SDK directly.
"""
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o")

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a technical writer."),
    ("user", "{topic}"),
])

chain = prompt | llm


def write_article(topic: str) -> str:
    return chain.invoke({"topic": topic}).content
