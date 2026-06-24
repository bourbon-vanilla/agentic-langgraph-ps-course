# Langgraph Pluralsight Course

__Pluralsight Course Link__: [LangGraph Essentials for Developers](https://app.pluralsight.com/library/courses/langgraph-essentials-developers)

## Project Overview

This project contains the codebase for a Pluralsight course on **LangGraph**. It covers building LLM-powered workflows and agents using LangGraph, LangChain, and OpenAI.

- **Python version**: 3.13 (managed via `uv`)
- **Package manager**: `uv` (uses `pyproject.toml` and `uv.lock`)
- **Core dependencies**: `langgraph`, `langchain`, `ipykernel`, `jupyter`
- **LLM provider**: OpenAI (`gpt-4o-mini` is the default model)

## Project Structure

```
langgraph-ps-course/
├── 01/..07/            # Per-module demo code (course lectures)
│   └── demos/
│       └── ModuleN/
│           ├── clip*_*.py     # Python scripts (named clipX_Y_)
│           ├── *.ipynb         # Jupyter notebooks
│           ├── .env            # Per-module env file (API keys)
│           └── requirements.txt
├── pyproject.toml      # Project metadata, deps
├── .python-version     # Python 3.13
├── uv.lock             # Lock file (uv-managed)
└── .venv/              # Virtual environment (gitignored)
```

### Module Topics

| Module | Topic | Key Patterns |
|--------|-------|-------------|
| 01 | State, Graph,Reducers | `StateGraph`, `TypedDict` state, reducers (`add_messages`, custom), `START`/`END` |
| 02 | Workflows | Sequential, parallel, conditional edges, iterative, evaluator patterns |
| 03 | LLM Agents | Chatbots, tool calling, ReAct pattern, multi-agent, `create_agent` |
| 04 | Memory & Persistence | `MemorySaver`, `SqliteSaver`, `thread_id` config, fault tolerance |
| 05 | Human-in-the-Loop | `interrupt()`, `Command` routing, approval workflows, feedback loops |
| 06 | UI Deployment | Streamlit UI, `app.py` + `graph_backend.py` separation |
| 07 | Production | LangSmith tracing, evaluation, `LANGSMITH_PROJECT` env var |

## How to Run

### Environment setup

```bash
# Activate the virtual environment
uv venv && source .venv/bin/activate   # or uv sync

# Set API keys (each module has its own .env)
# Edit the .env in the module's demos/ModuleN/ directory:
# OPENAI_API_KEY="sk-..."
# TAVILY_API_KEY="tvly-..."
```

### Running a demo script

```bash
uv run python 02/demos/Module2/clip1_1_sequential.py
# or (if venv is activated)
python 02/demos/Module2/clip1_1_sequential.py
```

### Running a notebook

```bash
jupyter notebook 01/demos/Module1/clip3_2_email_visualize_notebook.ipynb
```

### Module 6 (Streamlit)

```bash
cd 06/demos/Module6
streamlit run app.py
```

## Code Conventions

### File Naming

- Python scripts follow the pattern: `clip{X}_{Y}_{description}.py`
  - `X` = clip number within the module
  - `Y` = variation number
  - Example: `clip2_1_sequential.py`, `clip4_2_returning_labels.py`
- Case varies: some use lowercase (`clip1_1_...`), some mixed (`Clip1_1_...`). When creating new files, use **lowercase** for consistency.

### State Definition

```python
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, add_messages, START, END

class MyState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    topic: str
    result: str
```

- Always use `TypedDict` for state (not `dict`)
- For chat/message state, use `Annotated[list[AnyMessage], add_messages]` reducer
- For plain accumulation, use custom reducers

### Node Functions

```python
def my_node(state: MyState):
    # Always read from state, return partial dict of updated keys
    return {"some_key": new_value}
```

- Nodes receive the full state `dict`, return only the keys being updated
- Return values are merged/merged-by-reducer into state, not replacing the whole state

### Graph Construction Pattern

```python
graph_builder = StateGraph(MyState)

# Register nodes
graph_builder.add_node("node_name", node_func)

# Wire edges
graph_builder.add_edge(START, "first_node")
graph_builder.add_edge("first_node", "second_node")
graph_builder.add_conditional_edges("decision_node", router_func, {"route_a": "node_a", "route_b": END})
graph_builder.add_edge("last_node", END)

# Compile
graph = graph_builder.compile()
# For persistence:
graph = graph_builder.compile(checkpointer=MemorySaver())
```

- Always use `StateGraph(STATE_CLASS)` — pass the state typed dict class
- Import: `from langgraph.graph import StateGraph, START, END`
- Variable naming: use `graph_builder` for the builder, `graph` for the compiled graph

### LLM Setup

```python
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()
llm = ChatOpenAI(model="gpt-4o-mini")
```

- Always call `load_dotenv()` before instantiating the LLM
- Default model is `gpt-4o-mini`
- When tools are needed, use `llm.bind_tools(tools)`

### Tool Definition

```python
from langchain_core.tools import tool

@tool
def my_tool(param: int) -> str:
    """Description of what the tool does (used by the LLM)."""
    return result
```

- Use `@tool` decorator from `langchain_core.tools`
- Include a docstring — it becomes the tool description for the LLM
- Build lookup dict: `tools_by_name = {tool.name: tool for tool in tools}`

### Environment Variables

- API keys are stored in `.env` files per module directory
- **Never commit actual API keys** — the repo templates have placeholder values
- Variables used: `OPENAI_API_KEY`, `TAVILY_API_KEY`, `LANGSMITH_API_KEY`, `LANGSMITH_PROJECT`

## Creating New Demos

When adding a new demo for a module:

1. Create the file inside the correct `0N/demos/ModuleN/` directory
2. Follow the `clipX_Y_description.py` naming convention (lowercase)
3. Include a docstring comment at the top describing the demo
4. Load `.env` with `load_dotenv()` at the top
5. Define state, nodes, wire graph, compile, invoke
6. Print output for verification at the end

```python
# Brief description of what this demo shows

from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv

load_dotenv()

# ... state, nodes, graph wiring, invocation ...
```

## Common Patterns to Know

### Sequential Workflow (Module 2)
Multiple nodes chained linearly: `START → A → B → C → END`

### Parallel Workflow (Module 2)
Multiple nodes branching from one point, converging later:
`START → A, B, C → merge → END`

### Conditional Routing (Module 2)
A router function decides the next node. Return a string label matching the mapping dict.

### ReAct Agent (Module 3)
`chatbot → should_continue → tool_node → chatbot` loop. The router checks `tool_calls` on the last message.

### Memory/Checkpointer (Module 4)
Pass `checkpointer=MemorySaver()` or `SqliteSaver(conn)` to `compile()`. Use `config = {"configurable": {"thread_id": "..."}}` with `invoke()`.

### Human-in-the-Loop (Module 5)
Use `interrupt()` to pause execution. Resume with `Command(resume=value)`. Requires a checkpointer.

### Command Routing (Module 5)
Return `Command(goto="node_name", update={...})` from a node for direct routing control.

## Important Imports Reference

```python
# Core graph
from langgraph.graph import StateGraph, START, END, add_messages

# State typing
from typing import TypedDict, Annotated, Literal

# LLM
from langchain_openai import ChatOpenAI

# Messages
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage, AnyMessage

# Tools
from langchain_core.tools import tool

# Memory / Checkpointers
from langgraph.checkpoint.memory import MemorySaver
from langgraph.checkpoint.sqlite import SqliteSaver

# Human-in-the-loop
from langgraph.types import interrupt, Command

# Environment
from dotenv import load_dotenv
```

## Safety Rules

- **Never commit real API keys**. If an `.env` file contains a real key, redact it.
- **Never hardcode API keys** in source files — always use `load_dotenv()`
- When generating code, use placeholder keys like `"sk-placeholder-..."` if needed
- Prefer `pyproject.toml` dependencies over per-module `requirements.txt` for new code
