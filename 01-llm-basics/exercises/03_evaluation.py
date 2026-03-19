"""
Exercise: Basic evaluation

Goal: Evaluate your prompt against a small dataset to see how well it performs.
This introduces ragbits' evaluation framework - you'll use it more in later lessons.

Run:  python 03_evaluation.py

Note: This exercise uses MODEL_SMART as the judge model because evaluating
answer quality requires a more capable model than generating answers.
"""

import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))
from config import MODEL, MODEL_SMART

from pydantic import BaseModel
from ragbits.agents.types import QuestionAnswerAgent
from ragbits.core.llms import LiteLLM
from ragbits.core.prompt import Prompt
from ragbits.core.sources import WebSource
from ragbits.evaluate.dataloaders.question_answer import QuestionAnswerDataLoader
from ragbits.evaluate.evaluator import Evaluator
from ragbits.evaluate.metrics import MetricSet
from ragbits.evaluate.metrics.question_answer import QuestionAnswerAnswerCorrectness
from ragbits.evaluate.pipelines.question_answer import QuestionAnswerPipeline


# --- Step 1: Define the prompt (same pattern as before) ---

class QuestionInput(BaseModel):
    question: str

class ReasonedAnswer(BaseModel):
    reasoning: str
    answer: str

class QAPrompt(Prompt[QuestionInput, ReasonedAnswer]):
    system_prompt = """
    You are a question answering agent. Answer the question to the best of your ability.
    Think step by step.
    """
    user_prompt = """
    Question: {{ question }}
    """


async def main() -> None:
    # --- Step 2: Create the agent ---
    llm = LiteLLM(model_name=MODEL, use_structured_output=True)
    agent = QuestionAnswerAgent(llm=llm, prompt=QAPrompt)

    # --- Step 3: Load a test dataset ---
    # This loads 20 tech Q&A pairs from a public dataset
    source = WebSource(
        url="https://huggingface.co/datasets/deepsense-ai/ragbits/resolve/main/ragqa_arena_tech_examples.jsonl"
    )
    dataloader = QuestionAnswerDataLoader(
        source=source,
        split="data[:20]",  # just 20 examples to keep it quick
        question_key="question",
        answer_key="response",
    )

    # TODO 1: Load the dataset and print the first item to see what it looks like
    # dataset = await dataloader.load()
    # print(dataset[0])

    # --- Step 4: Set up the metric ---
    # The judge model evaluates how correct the answers are
    judge = LiteLLM(model_name=MODEL_SMART)
    metric = QuestionAnswerAnswerCorrectness(judge)

    # --- Step 5: Run evaluation ---
    # TODO 2: Create an Evaluator and run it
    # evaluator = Evaluator()
    # results = await evaluator.compute(
    #     dataloader=dataloader,
    #     pipeline=QuestionAnswerPipeline(agent),
    #     metricset=MetricSet(metric),
    # )
    # print(f"Answer correctness: {results.metrics}")


if __name__ == "__main__":
    asyncio.run(main())
