"""
Exercise: Agent with MCP tools

Goal: Use the Model Context Protocol to give your agent the ability to
fetch and read web pages - without writing any tool code yourself.

Prerequisites:
  pip install mcp-server-fetch

Run:  python 02_mcp_agent.py
"""

import asyncio
import sys

sys.path.append("../..")
from config import MODEL

from pydantic import BaseModel
from ragbits.agents import Agent
from ragbits.agents.mcp import MCPServerStdio
from ragbits.core.llms import LiteLLM
from ragbits.core.prompt import Prompt


# --- Step 1: Define the prompt ---

class ResearchInput(BaseModel):
    question: str


# TODO 1: Create a prompt for a research assistant.
# The system prompt should mention that the agent can fetch web pages.
#
# class ResearchPrompt(Prompt[ResearchInput, str]):
#     system_prompt = """
#     You are a research assistant that can look up information online.
#     When the user asks about a topic, use your web fetching tool to
#     find relevant information and summarize it.
#     """
#     user_prompt = "{{ question }}"


async def main() -> None:
    # --- Step 2: Create the agent with MCP ---

    # TODO 2: Create an agent that uses the mcp-server-fetch MCP server.
    # The MCP server gives the agent a `fetch` tool for reading web pages.
    #
    # agent = Agent(
    #     llm=LiteLLM(model_name=MODEL),
    #     prompt=ResearchPrompt,
    #     mcp_servers=[
    #         MCPServerStdio(command="python", args=["-m", "mcp_server_fetch"]),
    #     ],
    # )

    # TODO 3: Test it! Ask something that requires looking up info online.
    # async with agent:
    #     result = await agent.run(ResearchInput(
    #         question="What is ragbits? Look up https://ragbits.deepsense.ai/ and summarize it."
    #     ))
    #     print(result.content)

    # TODO 4 (bonus): Try asking it to compare two web pages, or to
    # look up something specific from a documentation site.
    pass


if __name__ == "__main__":
    asyncio.run(main())
