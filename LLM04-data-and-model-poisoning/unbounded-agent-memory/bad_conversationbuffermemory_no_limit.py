"""ConversationBufferMemory keeps every turn forever, with no limit.

Triggers unbounded-agent-memory: no window size (k) or token limit is
configured, so memory (and prompt/token cost, and the attack surface
for stuffing/poisoning past turns) grows without bound as the session
continues.
"""
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI

memory = ConversationBufferMemory()  # no k, no max_token_limit
chain = ConversationChain(llm=ChatOpenAI(model="gpt-4o"), memory=memory)


def chat(message: str):
    return chain.predict(input=message)
