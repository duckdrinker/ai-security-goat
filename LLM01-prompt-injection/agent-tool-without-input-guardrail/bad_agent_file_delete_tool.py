import os
from langchain.agents import Tool, initialize_agent
from langchain_openai import ChatOpenAI


def delete_file(path: str) -> str:
    # Filesystem path chosen entirely by the LLM is deleted with no path allow-list, confirmation, or sandbox boundary
    os.remove(path)
    return f"Deleted {path}"


tools = [Tool(name="delete_file", func=delete_file, description="Delete a file by path")]
llm = ChatOpenAI(model="gpt-4o")
agent = initialize_agent(tools, llm, agent="zero-shot-react-description")
agent.run("Clean up old log files in the workspace.")
