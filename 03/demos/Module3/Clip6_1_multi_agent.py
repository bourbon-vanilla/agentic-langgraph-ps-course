# A multi-agent system where a controller agent delegates tasks to specialized math and research agents
import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch
from langchain.tools import tool
from langchain.agents import create_agent

load_dotenv()

llm = ChatOpenAI(
    model=os.environ["CUSTOM_OPENAI_MODEL"],
    base_url=os.environ["CUSTOM_OPENAI_ENDPOINT"],
    api_key=os.environ["CUSTOM_OPENAI_API_KEY"],
)

# =======================
# Sub-Agent 1: Math Agent
# =======================

@tool(description="Add two numbers and return the sum.")
def add(a: int, b: int) -> int:
    """Add a and b."""
    return a + b

@tool("subtract", description="Subtract b from a and return the result.")
def sub(a: int, b: int) -> int:
    """Return a - b."""
    return a - b

math_agent = create_agent(
    model=llm,
    tools=[add, sub],
    system_prompt="""You are a math expert. Always use the provided tools for calculations and respond in plain text only."""
)

@tool("math_helper", description="Use this for arithmetic questions.")
def call_math_agent(query: str) -> str:
    result = math_agent.invoke({"messages": [{"role": "user", "content": query}]})
    return result["messages"][-1].content


# ===========================
# Sub-Agent 2: Research Agent
# ===========================

tavily_tool = TavilySearch(max_results=2)

research_agent = create_agent(
    model=llm,
    tools=[tavily_tool],
    system_prompt="""You are a research specialist. Always use TavilySearch for factual and recent information."""
)

@tool("search_helper", description="Use this to retrieve up-to-date information from the web.")
def call_research_agent(query: str) -> str:
    result = research_agent.invoke({"messages": [{"role": "user", "content": query}]})
    return result["messages"][-1].content


# ======================
# Main Controller Agent
# ======================

controller_agent = create_agent(
    model=llm,
    tools=[call_math_agent, call_research_agent],
    system_prompt="""You are a controller agent. Decide which agent should perform the task. 
Always provide the final answer in plain natural language."""
)


# ============
# Test Queries
# =============

queries = [
    "What is 56 - 19?",
    "What is the young one of a cat called",
    "Add 5 to the temperature in Bangalore today.",
]

for q in queries:
    print(f"\nUser: {q}")
    response = controller_agent.invoke({ "messages": [{"role": "user", "content": q}]})
    final_answer = response["messages"][-1].content
    print("Assistant:", final_answer)


for q in queries:
    print(f"\nUser: {q}")
    response = controller_agent.invoke({ "messages": [{"role": "user", "content": q}]})
    for message in response["messages"]:
        message.pretty_print()