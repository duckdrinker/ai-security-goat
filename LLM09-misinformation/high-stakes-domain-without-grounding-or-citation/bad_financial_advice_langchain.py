"""
Triggers high-stakes-domain-without-grounding-or-citation: a LangChain chain
gives financial/investment advice straight from the LLM, with no retriever
in the chain and no instruction to cite sources for its recommendations.
"""
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o")

prompt = ChatPromptTemplate.from_messages([
    ("system", (
        "You are a financial advisor. Give the user financial advice on how "
        "to allocate their retirement savings across asset classes."
    )),
    ("user", "{question}"),
])

financial_advice_chain = prompt | llm


def get_financial_advice(question: str) -> str:
    result = financial_advice_chain.invoke({"question": question})
    return result.content
