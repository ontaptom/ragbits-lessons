"""
Exercise: Connect to a remote MCP server

Goal: Use a publicly hosted MCP server (DeepWiki) to give your agent
the ability to look up information about any public GitHub repository -
no extra installs, no API keys, just a URL.

This shows the difference between local MCP (exercise 02, stdio) and
remote MCP (HTTP) - in production, MCP servers are typically standalone
services you connect to over the network.

Run:  python 03_external_mcp_agent.py
"""

import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))
from config import MODEL_SMART

from pydantic import BaseModel
from ragbits.agents import Agent, ToolCallResult
from ragbits.agents.mcp import MCPServerStreamableHttp
from ragbits.core.llms import LiteLLM, ToolCall
from ragbits.core.prompt import Prompt


# --- The prompt and MCP server are ready to go ---

class ResearchInput(BaseModel):
    question: str


class ResearchPrompt(Prompt[ResearchInput, str]):
    system_prompt = """
    You are a research assistant that can look up information about open source
    projects on GitHub. Use your tools to find relevant information and
    provide clear, concise answers.
    """
    user_prompt = "{{ question }}"


async def main() -> None:
    # DeepWiki is a free, public MCP server - no auth needed.
    # It provides tools to browse and ask questions about any public GitHub repo.
    # We connect to it over HTTP using MCPServerStreamableHttp.
    server = MCPServerStreamableHttp(
        params={"url": "https://mcp.deepwiki.com/mcp", "timeout": 30},
        client_session_timeout_seconds=30,
    )

    async with server:

        # TODO 1: Create an Agent that uses the MCP server.
        # You need:
        #   - LiteLLM with MODEL_SMART
        #   - ResearchPrompt as the prompt
        #   - the server in mcp_servers list
        #   - keep_history=True so the agent remembers previous messages
        #
        # agent = Agent(...)

        # TODO 2: Build a chat loop.
        # Read user input, call agent.run(), print the response.
        # Exit when the user types "quit" or "exit".
        #
        # Try asking:
        #   "What is deepsense-ai/ragbits?"
        #   "How does it compare to langchain-ai/langchain?"
        #   (the agent should remember the context from the first question)
        #
        # Hint: agent.run() returns a result with a .content attribute.

        # BONUS: Replace agent.run() with agent.run_streaming() to see
        # tool calls happening in real time. You can use match/case on the
        # streamed events:
        #
        #   async for event in agent.run_streaming(ResearchInput(question=...)):
        #       match event:
        #           case ToolCall():
        #               print(f"  -> Calling tool: {event.name}({event.arguments})")
        #           case ToolCallResult():
        #               preview = str(event.result)[:200]
        #               print(f"  <- Tool result: {preview}...")
        #           case str():
        #               if event.strip():
        #                   print(event, end="", flush=True)
        pass


if __name__ == "__main__":
    asyncio.run(main())
