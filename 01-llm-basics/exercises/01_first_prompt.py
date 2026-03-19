"""
Exercise: Your first ragbits prompt

Goal: Define a prompt, send it to an LLM, and print the response.

Run:  python 01_first_prompt.py
"""

import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))
from config import MODEL

from pydantic import BaseModel
from ragbits.core.llms import LiteLLM
from ragbits.core.prompt import Prompt


# TODO 1: Create a Pydantic model for the prompt input.
# It should have a single field: `question` (str)


# TODO 2: Create a Prompt class called `SimpleQAPrompt`
# - Input type: your model from TODO 1
# - Output type: str (just raw text)
# - system_prompt: something like "You are a helpful assistant that answers questions."
# - user_prompt: use Jinja2 template syntax: "{{ question }}"
#
# Example:
#   class SimpleQAPrompt(Prompt[YourInputModel, str]):
#       system_prompt = "..."
#       user_prompt = "{{ question }}"


async def main() -> None:
    llm = LiteLLM(model_name=MODEL)

    # TODO 3: Create a prompt instance with a question of your choice
    # prompt = SimpleQAPrompt(YourInputModel(question="..."))

    # TODO 4: Call llm.generate(prompt) and print the response
    pass


if __name__ == "__main__":
    asyncio.run(main())
