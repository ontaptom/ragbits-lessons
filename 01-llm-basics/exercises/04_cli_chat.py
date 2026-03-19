"""
Exercise: Build a simple CLI chatbot

Goal: Put your prompt skills to use - build a terminal chat loop that
talks to an LLM. This is the "manual" way to build a chat experience.
In the next lesson, you'll see how ragbits gives you a web UI for free.

Run:  python 04_cli_chat.py
"""

import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))
from config import MODEL

from pydantic import BaseModel
from ragbits.core.llms import LiteLLM
from ragbits.core.prompt import Prompt


# TODO 1: Create a prompt class for your chatbot.
# Reuse the pattern from exercise 01 - input model + Prompt class.
# Pick a personality that makes it fun to chat with.
#
# class ChatInput(BaseModel):
#     question: str
#
# class ChatPrompt(Prompt[ChatInput, str]):
#     system_prompt = "..."
#     user_prompt = "{{ question }}"


async def main() -> None:
    llm = LiteLLM(model_name=MODEL)

    # TODO 2: Build a chat loop.
    # Read user input, send it to the LLM, print the response.
    # Exit when the user types "quit" or "exit".
    #
    # print("Chat started! Type 'quit' or 'exit' to stop.\n")
    # while True:
    #     user_input = input("You: ")
    #     if user_input.strip().lower() in ("quit", "exit"):
    #         print("Bye!")
    #         break
    #     prompt = ChatPrompt(ChatInput(question=user_input))
    #     response = await llm.generate(prompt)
    #     print(f"Bot: {response}\n")


if __name__ == "__main__":
    asyncio.run(main())
