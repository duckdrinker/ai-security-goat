from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o")


def analyze_uploaded_pdf(file_path: str, question: str) -> str:
    loader = PyPDFLoader(file_path)
    pages = loader.load()
    # Text extracted from a user-uploaded PDF is passed directly into the prompt with no content filtering
    document_text = "\n".join(p.page_content for p in pages)
    prompt = f"Document:\n{document_text}\n\nAnswer this question about the document: {question}"
    return llm.invoke(prompt).content
