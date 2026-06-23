# HITL example with human approval using interrupt()

from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, add_messages, START, END
from langgraph.types import interrupt, Command
from langchain_core.messages import HumanMessage, SystemMessage, AnyMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from typing import Literal
from dotenv import load_dotenv

load_dotenv()

class State(TypedDict):
    topic: str
    messages: Annotated[list[AnyMessage], add_messages]
    approval: str

llm = ChatOpenAI(model="gpt-4o-mini")

def create_tweet(state: State):
    response = llm.invoke([
        SystemMessage("You are an expert at writing engaging tweets"),
        HumanMessage(f"Write a tweet on {state['topic']}")
    ])
    print("Tweet generated")
    return {"messages": response}

def human_review(state: State):
    print("Human review node executing....")

    # Human input expected as a string: "yes" or "no"
    human_input = interrupt({
        "tweet": state["messages"][-1].content,
        "question": "Do you want to post this tweet? (yes/no)"
    })
    return {"approval": human_input}

def review_router(state: State)-> Literal["post_tweet", "__end__"]:
    if state["approval"].lower() == "yes":
        return "post_tweet"
    else:
        return END

def post_tweet(state: State):
    print("\nTweet posted\n")
    print(state["messages"][-1].content)
    return {}

graph_builder = StateGraph(State)

graph_builder.add_node("create_tweet", create_tweet)
graph_builder.add_node("human_review", human_review)
graph_builder.add_node("post_tweet", post_tweet)

graph_builder.add_edge(START, "create_tweet")
graph_builder.add_edge("create_tweet", "human_review")
graph_builder.add_conditional_edges("human_review", review_router)
graph_builder.add_edge("post_tweet", END)

graph = graph_builder.compile(checkpointer=MemorySaver())

# Run the workflow
config = {"configurable": {"thread_id": "demo-1"}}
result = graph.invoke({"topic": "Life"}, config=config)

# -------------------------
# UI simulation (display interrupt payload)
# -------------------------
payload = result["__interrupt__"][0].value

print("\n" + "=" * 50)
print("HUMAN REVIEW SCREEN")
print("=" * 50)

print("\nGenerated Tweet:\n")
print(payload["tweet"])

print("\nQuestion:")
print(payload["question"])

print("\nWaiting for human response...")
print("=" * 50)

# --- Simulated UI input ---
human_response = "yes"   # imagine this comes from a UI, it can be a "no" 
print("\nHuman selected:", human_response)
print("Sending response back to workflow...\n")

# Re-invoke the graph with user response
graph.invoke(Command(resume=human_response), config=config)