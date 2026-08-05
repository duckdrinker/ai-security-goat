"""
Triggers agent-loop-without-iteration-cap: LangChain's AgentExecutor exposes
`max_iterations` specifically to bound the agent loop, and it is explicitly
set to None here (equivalent to omitting it) — LangChain will let the
reasoning/tool cycle run without limit until the model itself decides to
stop.
"""
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from my_tools import TOOLS

llm = ChatOpenAI(model="gpt-4o")
prompt = PromptTemplate.from_template(
    "Answer the question using the available tools.\n\nQuestion: {input}\n{agent_scratchpad}"
)
agent = create_react_agent(llm, TOOLS, prompt)

executor = AgentExecutor(
    agent=agent,
    tools=TOOLS,
    max_iterations=None,  # unbounded: no ceiling on the reasoning/tool loop
    verbose=True,
)


def run(task: str) -> str:
    return executor.invoke({"input": task})["output"]
