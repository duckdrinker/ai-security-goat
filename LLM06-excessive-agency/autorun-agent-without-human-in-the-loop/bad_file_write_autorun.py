"""
Triggers autorun-agent-without-human-in-the-loop: a LangChain AgentExecutor
runs with max_iterations set high and no HumanApprovalCallbackHandler (or any
other confirmation step) wired in, yet one of its tools has a side effect
(overwriting a file on disk). The agent can loop and write files unattended.
"""
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.tools import Tool
from langchain_openai import ChatOpenAI


def write_report(args: str) -> str:
    path, content = args.split("|", 1)
    with open(path, "w") as f:
        f.write(content)
    return f"wrote {path}"


tools = [
    Tool.from_function(
        func=write_report,
        name="write_report",
        description="Write a report file to disk. Args: 'path|content'.",
    )
]

llm = ChatOpenAI(model="gpt-4o", temperature=0)
agent = create_openai_tools_agent(llm, tools, prompt=None)

# autonomous=True and no callbacks -> the agent can invoke write_report as
# many times as it wants across up to 25 iterations with zero human checkpoint.
executor = AgentExecutor(
    agent=agent,
    tools=tools,
    autonomous=True,
    max_iterations=25,
    verbose=False,
)

executor.invoke({"input": "Generate the quarterly report and save it wherever you think is best."})
