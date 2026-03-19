"""
Exercise: Structured output with chain-of-thought

Goal: Get the LLM to return structured data (not just a string).
We'll use chain-of-thought prompting to make the model reason before answering.

Run:  python 02_structured_output.py
"""

import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))
from config import MODEL

from pydantic import BaseModel
from ragbits.core.llms import LiteLLM
from ragbits.core.prompt import Prompt


class QuestionInput(BaseModel):
    question: str


# TODO 1: Create an output model called `ReasonedAnswer` with two fields:
#   - reasoning: str  (the model's step-by-step thinking)
#   - answer: str     (the final answer)


# TODO 2: Create a Prompt class called `ChainOfThoughtPrompt`
#   - Input type: QuestionInput
#   - Output type: ReasonedAnswer (your model from TODO 1)
#   - system_prompt: tell the model to think step by step
#   - user_prompt: "Question: {{ question }}"


async def main() -> None:
    # Note: use_structured_output=True tells the LLM to return JSON
    # matching your output model's schema
    llm = LiteLLM(model_name=MODEL, use_structured_output=True)

    # TODO 3: Create a prompt asking something that requires reasoning.
    # Some fun ideas:
    #   - "If I have 3 boxes, each with 2 cats, and each cat has 4 kittens, how many animals total?"
    #   - "Is it possible to tile a 8x8 chessboard with 2x1 dominoes if two opposite corners are removed?"
    # prompt = ChainOfThoughtPrompt(QuestionInput(question="..."))

    # TODO 4: Generate the response and print both reasoning and answer separately
    # response = await llm.generate(prompt)
    # print("Reasoning:", response.reasoning)
    # print("Answer:", response.answer)
    pass


if __name__ == "__main__":
    asyncio.run(main())
