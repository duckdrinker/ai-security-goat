"""Agent recalls persisted memories via similarity search, unfiltered.

Triggers persistent-context-injection: the top similarity results from
a persistent memory vector store are pasted straight into the prompt —
a memory entry poisoned in an earlier turn is retrieved and trusted
again with no revalidation.
"""
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

memory_store = Chroma(collection_name="agent_memory", embedding_function=OpenAIEmbeddings())
llm = ChatOpenAI(model="gpt-4o")


def recall_and_respond(query: str):
    memories = memory_store.similarity_search(query, k=3)
    context = "\n".join(m.page_content for m in memories)  # unfiltered recall of past-session content
    prompt = f"Relevant memories:\n{context}\n\nUser: {query}"
    return llm.invoke(prompt)
