"""
Triggers autorun-agent-without-human-in-the-loop: an AutoGen GroupChat of
multiple assistants deploys code to production through a registered function,
managed by a GroupChatManager whose executor proxy also has
human_input_mode="NEVER". The deploy tool fires as soon as any agent in the
chat decides it's warranted -- no human is ever asked to confirm the rollout.
"""
import autogen


def deploy_to_production(service: str, image_tag: str) -> str:
    import subprocess

    subprocess.run(["kubectl", "set", "image", f"deployment/{service}", f"{service}={image_tag}"], check=True)
    return f"deployed {service}:{image_tag}"


coder = autogen.AssistantAgent(name="coder", llm_config={"model": "gpt-4o"})
reviewer = autogen.AssistantAgent(name="reviewer", llm_config={"model": "gpt-4o"})

executor_proxy = autogen.UserProxyAgent(
    name="ops_executor",
    human_input_mode="NEVER",
    code_execution_config=False,
)

autogen.register_function(
    deploy_to_production,
    caller=coder,
    executor=executor_proxy,
    name="deploy_to_production",
    description="Deploy a container image to the production cluster.",
)

groupchat = autogen.GroupChat(agents=[coder, reviewer, executor_proxy], messages=[], max_round=15)
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config={"model": "gpt-4o"})

executor_proxy.initiate_chat(manager, message="Ship the latest hotfix build once you're both happy with it.")
