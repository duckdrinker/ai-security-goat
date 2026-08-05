"""
Triggers code-exec-tool-without-sandbox: AutoGen's UserProxyAgent is wired to
LocalCommandLineCodeExecutor, which runs model-generated code blocks with the
host shell in a plain working directory. AutoGen also ships
DockerCommandLineCodeExecutor for exactly this use case -- choosing the local
variant means every code block the assistant writes runs unsandboxed.
"""
import autogen
from autogen.coding import LocalCommandLineCodeExecutor

assistant = autogen.AssistantAgent(name="analyst", llm_config={"model": "gpt-4o"})

user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",
    code_execution_config={
        "executor": LocalCommandLineCodeExecutor(work_dir="./coding"),
    },
)

user_proxy.initiate_chat(assistant, message="Write and run a script to clean up the dataset in ./coding/data.csv.")
