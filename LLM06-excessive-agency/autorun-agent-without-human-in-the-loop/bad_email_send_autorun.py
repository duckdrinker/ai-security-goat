"""
Triggers autorun-agent-without-human-in-the-loop: an AutoGen UserProxyAgent is
configured with human_input_mode="NEVER" (fully autonomous, never pauses to
ask a human) and is wired to a function that sends real emails. Nothing stops
the assistant from deciding, on its own, to fire off outbound messages.
"""
import autogen

send_config = {"model": "gpt-4o"}


def send_email(to: str, subject: str, body: str) -> str:
    # real SMTP call in production; here it's the side-effecting sink
    import smtplib

    with smtplib.SMTP("smtp.internal.corp") as server:
        server.sendmail("agent@corp.com", [to], f"Subject: {subject}\n\n{body}")
    return f"sent to {to}"


assistant = autogen.AssistantAgent(name="outreach_bot", llm_config=send_config)

# human_input_mode="NEVER" means the proxy executes every function call the
# assistant proposes without ever surfacing it for approval.
user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    code_execution_config=False,
)

autogen.register_function(
    send_email,
    caller=assistant,
    executor=user_proxy,
    name="send_email",
    description="Send an email to a recipient.",
)

user_proxy.initiate_chat(
    assistant,
    message="Follow up with every lead in the CRM export and let them know about the new pricing.",
)
