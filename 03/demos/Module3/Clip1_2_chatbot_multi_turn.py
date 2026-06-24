# Multi-turn chat interface
import os

from typing import TypedDict, Annotated
from langgraph.graph import add_messages, StateGraph, START, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AnyMessage
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(
    model=os.environ["CUSTOM_OPENAI_MODEL"],
    base_url=os.environ["CUSTOM_OPENAI_ENDPOINT"],
    api_key=os.environ["CUSTOM_OPENAI_API_KEY"],
)

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

# Loop for multi-turn interaction
while True: 
    user_input = input("You: ")
    if(user_input.strip().lower() in ["stop", "exit", "end", "bye"]):
         print("Assistant: Goodbye!")
         break
    final_state = graph.invoke({"messages": [HumanMessage(content=user_input)] })
    last_message = final_state["messages"][-1] # Retrieve last AI response
    print("Assistant:", last_message.content)
    print()