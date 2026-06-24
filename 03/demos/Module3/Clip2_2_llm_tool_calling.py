# Shows how an LLM can decide when to call tools after binding them using bind_tools()
import os

from langchain_core.tools import tool
from langchain_tavily import TavilySearch
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()  

tavily_tool = TavilySearch(max_results=2)

@tool
def add(a: int, b: int) -> int:
    """
    Adds two numbers and returns the sum.
    Args:
        a: The first number to add
        b: The second number to add
    """
    return a + b

@tool("subtract", description="Subtract b from a and return the result.") 
def sub(a: int, b: int) -> int:
    """Return the difference of two numbers."""
    return a - b

llm = ChatOpenAI(
    model=os.environ["CUSTOM_OPENAI_MODEL"],
    base_url=os.environ["CUSTOM_OPENAI_ENDPOINT"],
    api_key=os.environ["CUSTOM_OPENAI_API_KEY"],
)

tools = [tavily_tool, add, sub]
llm_with_tools = llm.bind_tools(tools)

queries = ["Give one line definition of photosynthesis",
           "Who won the women's cricket world cup in 2025?",
           "Find the sum of 67 and 450",
           "Decrease 56 by 8",
           "What are the 7 colours in a rainbow",
           "What is the current price of bitcoin in USD",
]

for query in queries:
    print(query)
    response = llm_with_tools.invoke(query)
    print(response, end = "\n\n") 




