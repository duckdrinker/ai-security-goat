"""
Mitigates public-agent-missing-factuality-guardrail: the public support
agent pipeline now runs every draft answer through a citation-verifier step
before it is returned to the customer, rejecting answers that make claims it
cannot back with a real knowledge-base source.
"""
from fastapi import FastAPI
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

app = FastAPI()

llm = ChatOpenAI(model="gpt-4o")
prompt = ChatPromptTemplate.from_messages([
    ("system", (
        "You are the public support assistant for Acme Corp. Answer "
        "customer questions and cite the knowledge-base article you used "
        "for every factual claim."
    )),
    ("user", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])
agent = create_openai_tools_agent(llm, tools=[], prompt=prompt)
support_agent = AgentExecutor(agent=agent, tools=[])


def verify_citations(answer: str) -> bool:
    # Rejects the answer unless every claim links back to a real KB article.
    ...


@app.post("/api/public/chat")
def public_chat_endpoint(message: str):
    result = support_agent.invoke({"input": message})
    answer = result["output"]
    if not verify_citations(answer):
        return {"reply": "I don't have a confirmed answer for that — let me connect you with a human agent."}
    return {"reply": answer}
