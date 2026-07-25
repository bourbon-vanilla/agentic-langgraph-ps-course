# LangGraph Agent Quick Start

This folder contains a LangGraph agent configured in `langgraph.json`.

## Start the local host

From this directory, run:

```bash
langgraph dev
```

The CLI will start a local server and print a URL (typically `http://localhost:2024`).

## UI

You can try your agent in the ui. Simply call [agentchat.vercel.app/](https://agentchat.vercel.app/). A dialog will be presented to connect to your `http://localhost:2024`. Simply confirm the default values.

Read more in the [langchain doc pages](https://docs.langchain.com/oss/python/langchain/ui).

## Required setup

1. Copy `.env.template` to `.env` and fill in the required values.
2. Make sure your Python environment has the project dependencies installed
   `uv sync`
3. If you want to expose it on a specific host/port:

```bash
langgraph dev --host 0.0.0.0 --port 8000
```

## Notes

- The graph entrypoint is defined in `langgraph.json` and points to `src/agent.py:agent`.
- Press `Ctrl+C` in the terminal to stop the server.
