"""
Triggers public-agent-missing-factuality-guardrail: this customer-facing
support agent is wired straight from tools -> LLM -> HTTP response, exposed
on an unauthenticated public endpoint, with no factuality/citation guardrail
(NeMo Guardrails, a RAG-verifier chain, a citation-check callback, etc.)
anywhere in the pipeline.
"""
from fastapi import FastAPI
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

app = FastAPI()

llm = ChatOpenAI(model="gpt-4o")
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are the public support assistant for Acme Corp. Answer customer questions."),
    ("user", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])
agent = create_openai_tools_agent(llm, tools=[], prompt=prompt)
support_agent = AgentExecutor(agent=agent, tools=[])


@app.post("/api/public/chat")
def public_chat_endpoint(message: str):
    result = support_agent.invoke({"input": message})
    return {"reply": result["output"]}
