"""Mitigated: agent memory is explicitly bounded.

Either a fixed-size window (last N turns) or an explicit token cap
(older turns get summarized/dropped) is configured — memory can never
grow without bound.
"""
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferWindowMemory, ConversationTokenBufferMemory
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o")

# Option A: fixed number of turns.
window_memory = ConversationBufferWindowMemory(k=10)

# Option B: explicit token cap, older turns get summarized/dropped.
token_memory = ConversationTokenBufferMemory(llm=llm, max_token_limit=2000)

chain = ConversationChain(llm=llm, memory=window_memory)


def chat(message: str):
    return chain.predict(input=message)
