from langchain_classic.agents import (
    AgentExecutor,
    create_tool_calling_agent,
    tool,
)
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import create_agent

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant"),
        ("placeholder", "{chat_history}"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)
llm = ChatOllama(
    model="llama3.2:3b",
    temperature=0.1,
    max_tokens=1000,
)

@tool
def magic_function(input: int) -> int:
    """Applies a magic function to an input."""
    return input + 2

tools = [magic_function]

# agent = create_tool_calling_agent(llm, tools, prompt)
# agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)


agent_executor = create_agent(llm, tools=tools, system_prompt="execute magic_function")


answer = agent_executor.invoke({"input": "what is the value of magic_function(2)?"})
print(answer)

        # Using with chat history
        # from langchain_core.messages import AIMessage, HumanMessage
        # agent_executor.invoke(
        #     {
        #         "input": "what's my name?",
        #         "chat_history": [
        #             HumanMessage(content="hi! my name is bob"),
        #             AIMessage(content="Hello Bob! How can I assist you today?"),
        #         ],
        #     }
        # )