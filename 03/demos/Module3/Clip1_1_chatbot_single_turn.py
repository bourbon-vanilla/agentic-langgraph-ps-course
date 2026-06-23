# Single-turn chatbot

from typing import TypedDict, Annotated
from langgraph.graph import add_messages, StateGraph, START, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AnyMessage
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")

class ChatState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]

def chatbot(state: ChatState):
    response = llm.invoke(state["messages"])
    return { "messages": response}

graph_builder = StateGraph(ChatState)

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)

graph = graph_builder.compile()

user_input = input("You: ")
final_state = graph.invoke({"messages": [HumanMessage(content=user_input)] })
last_message = final_state["messages"][-1]
print("Assistant:", last_message.content)
