# HITL approval workflow using Command for routing and updates
# Using Command in clip6_1_tweet_feedback.py

from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, add_messages, START, END
from langgraph.types import interrupt, Command
from langchain_core.messages import HumanMessage, SystemMessage, AnyMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from dotenv import load_dotenv
from typing import Literal

load_dotenv()

class State(TypedDict):
    topic: str
    messages: Annotated[list[AnyMessage], add_messages]
    feedback: str  

llm = ChatOpenAI(model="gpt-4o-mini")

def create_tweet(state: State):
    response = llm.invoke([
        SystemMessage("You are an expert at writing engaging tweets"),
        HumanMessage(f"Write a tweet on {state['topic']}")
    ])
    return {"messages": response}


def human_review(state: State)-> Command[Literal["post_tweet", "incorporate_feedback"]]:
    print("Human review node executing...")

    human_input = interrupt({
        "tweet": state["messages"][-1].content,
        "question": "Approve this tweet? (yes / no + feedback)"
    })

    # Routing + state update happens HERE now
    if human_input["approval"].lower() == "yes":
        return Command(goto="post_tweet")
    else:
        return Command(
            update={"feedback": human_input.get("feedback", "")},
            goto="incorporate_feedback"
        )

# Rewrite tweet using feedback
def incorporate_feedback(state: State):
    print("\nIncorporating feedback...\n")

    tweet = state["messages"][-1].content
    response = llm.invoke([
        SystemMessage("You are an expert at writing engaging tweets"),
        HumanMessage(f"Rewrite this tweet:\n{tweet}\n\nFeedback: {state['feedback']}")
    ])
    return {"messages": response}


def post_tweet(state: State):
    print("\nTweet posted\n")
    print(state["messages"][-1].content)
    return {}


graph_builder = StateGraph(State)

graph_builder.add_node("create_tweet", create_tweet)
graph_builder.add_node("human_review", human_review)
graph_builder.add_node("incorporate_feedback", incorporate_feedback)
graph_builder.add_node("post_tweet", post_tweet)

graph_builder.add_edge(START, "create_tweet")
graph_builder.add_edge("create_tweet", "human_review")
graph_builder.add_edge("incorporate_feedback", "human_review")
graph_builder.add_edge("post_tweet", END)

graph = graph_builder.compile(checkpointer=MemorySaver())

with open("graph.png", "wb") as f:
    f.write(graph.get_graph().draw_mermaid_png())

# Run the workflow
config = {"configurable": {"thread_id": "demo-4"}}
result = graph.invoke({"topic": "Life"}, config=config)


# -------------------------
# UI simulation Loop
# -------------------------
while "__interrupt__" in result:
    payload = result["__interrupt__"][0].value

    print("\n" + "=" * 50)
    print("HUMAN REVIEW SCREEN")
    print("=" * 50)

    print("\nCurrent Tweet:\n")
    print(payload["tweet"])

    print("\nQuestion:")
    print(payload["question"])

    print("=" * 50)

    # --- Simulated UI input ---
    approval = input("\nApprove? (yes/no): ").strip().lower()
    feedback = ""

    if approval == "no":
        feedback = input("Provide feedback: ")

    print("\nSending response back to workflow...\n")

    result = graph.invoke(
        Command(resume={
            "approval": approval,
            "feedback": feedback
        }),
        config=config
    )
