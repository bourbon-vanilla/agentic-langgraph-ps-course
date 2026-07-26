import os, asyncio
# from datetime import datetime   
# from langchain.agents import create_agent
from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch
from deepagents import create_deep_agent

tavily_search_tool = TavilySearch(
    max_results=2,
    search_depth="basic"
)

# system_prompt = f"""You are a helpful assistant that can search the web for information using the search_web tool.
# When searching for searching for sport news only report formel 1 news.
# Today's date is {today}."""

# 1. Initialize your frontier model
llm = ChatOpenAI(
    model=os.environ["CUSTOM_OPENAI_MODEL"],
    base_url=os.environ["CUSTOM_OPENAI_ENDPOINT"],
    api_key=os.environ["CUSTOM_OPENAI_API_KEY"],
)

# 2. Add an environment tool (e.g., Google Search built-in tool dict)
@tool
async def search_web(query: str) -> str:
    """Search for general web results."""
    return await asyncio.to_thread(tavily_search_tool.invoke, {"query": query})

tools = [search_web]

# 3. Create the agent harness — LangGraph is built automatically under the hood
agent = create_deep_agent(
    model=llm,
    tools=tools,
    system_prompt="You are an advanced researcher looking up complex data."
)
