import os, asyncio
from datetime import datetime   
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch

tavily_search_tool = TavilySearch(
    max_results=2,
    search_depth="basic"
)

@tool
async def search_web(query: str) -> str:
    """Search for general web results."""
    return await asyncio.to_thread(tavily_search_tool.invoke, {"query": query})

tools = [search_web]

today = datetime.now().strftime("%Y-%m-%d")

system_prompt = f"""You are a helpful assistant that can search the web for information using the search_web tool.
When searching for searching for sport news only report formel 1 news.
Today's date is {today}."""

llm = ChatOpenAI(
    model=os.environ["CUSTOM_OPENAI_MODEL"],
    base_url=os.environ["CUSTOM_OPENAI_ENDPOINT"],
    api_key=os.environ["CUSTOM_OPENAI_API_KEY"],
)

agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=system_prompt,
)
