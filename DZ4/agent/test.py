from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage

llm = ChatOllama(
    model="llama3.2:3b",
    temperature=0.1,
    max_tokens=1000,
)

answer = llm.invoke([HumanMessage(content='hello')])

print(answer)


