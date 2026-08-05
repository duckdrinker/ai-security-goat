from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI

vectorstore = FAISS.load_local("kb_index", OpenAIEmbeddings())
llm = ChatOpenAI(model="gpt-4o")


def answer_question(question: str) -> str:
    docs = vectorstore.similarity_search(question, k=4)
    # Retrieved document chunks (potentially attacker-controlled, e.g. via an uploaded file) are concatenated straight into the prompt
    context = "\n\n".join(d.page_content for d in docs)
    prompt = f"Context:\n{context}\n\nQuestion: {question}"
    return llm.invoke(prompt).content
