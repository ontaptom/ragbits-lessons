"""
Exercise: Build a full RAG pipeline

Goal: Combine retrieval + generation into a single agent, then evaluate it.
Compare the score with the plain LLM from lesson 01!

Run:  python 03_rag_agent.py

Make sure you ran 01_ingest.py first (we need the vector index).
"""

import asyncio
import sys
from collections.abc import Sequence
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))
from config import MODEL, MODEL_SMART, EMBEDDING_MODEL

from pydantic import BaseModel
from qdrant_client import AsyncQdrantClient
from ragbits.agents import AgentOptions, AgentResult
from ragbits.agents.types import QuestionAnswerAgent
from ragbits.core.embeddings import LiteLLMEmbedder
from ragbits.core.llms import LiteLLM
from ragbits.core.prompt import Prompt
from ragbits.core.sources import WebSource
from ragbits.core.vector_stores import VectorStoreOptions
from ragbits.core.vector_stores.qdrant import QdrantVectorStore
from ragbits.document_search import DocumentSearch
from ragbits.document_search.documents.element import Element
from ragbits.evaluate.dataloaders.question_answer import QuestionAnswerDataLoader
from ragbits.evaluate.evaluator import Evaluator
from ragbits.evaluate.metrics import MetricSet
from ragbits.evaluate.metrics.question_answer import QuestionAnswerAnswerCorrectness
from ragbits.evaluate.pipelines.question_answer import QuestionAnswerPipeline


# --- Step 1: Set up the retriever (same as 01_ingest.py) ---

retriever = DocumentSearch(
    vector_store=QdrantVectorStore(
        client=AsyncQdrantClient(path="./ragqa_arena_tech_corpus"),
        embedder=LiteLLMEmbedder(model_name=EMBEDDING_MODEL),
        default_options=VectorStoreOptions(k=5),
        index_name="ragqa_arena_tech_corpus",
    ),
)


# --- Step 2: Define the RAG prompt ---

class QuestionInput(BaseModel):
    question: str
    context: Sequence[Element] | None = None

class ReasonedAnswer(BaseModel):
    reason: str
    answer: str

# TODO 1: Create a RAG prompt class.
# Similar to the CoT prompt from lesson 01, but now include context.
#
# class RAGPrompt(Prompt[QuestionInput, ReasonedAnswer]):
#     system_prompt = """
#     You are a question answering agent. Answer the question using the provided context.
#     If the context doesn't have enough information, say so.
#     Think step by step.
#     """
#     user_prompt = """
#     Question: {{ question }}
#     Context: {% for chunk in context %}{{ chunk.text_representation }}{% endfor %}
#     """


# --- Step 3: Create the RAG agent ---

# TODO 2: Create an agent class that does retrieval before generation.
#
# class RAGQAAgent(QuestionAnswerAgent):
#     async def run(self, input: QuestionInput, options: AgentOptions | None = None) -> AgentResult[ReasonedAnswer]:
#         context = await retriever.search(input.question)
#         return await super().run(QuestionInput(question=input.question, context=context))


async def main() -> None:
    llm = LiteLLM(model_name=MODEL, use_structured_output=True)

    # TODO 3: Create the RAG agent
    # rag = RAGQAAgent(llm=llm, prompt=RAGPrompt)

    # TODO 4: Test it with a single question first
    # response = await rag.run(QuestionInput(question="What are high memory and low memory on linux?"))
    # print(response.content.answer)

    # TODO 5: Run evaluation (same dataset as lesson 01, 20 examples)
    # Compare the score with what you got in lesson 01!
    #
    # source = WebSource(
    #     url="https://huggingface.co/datasets/deepsense-ai/ragbits/resolve/main/ragqa_arena_tech_examples.jsonl"
    # )
    # dataloader = QuestionAnswerDataLoader(
    #     source=source,
    #     split="data[:20]",
    #     question_key="question",
    #     answer_key="response",
    # )
    # judge = LiteLLM(model_name=MODEL_SMART)
    # metric = QuestionAnswerAnswerCorrectness(judge)
    #
    # evaluator = Evaluator()
    # results = await evaluator.compute(
    #     dataloader=dataloader,
    #     pipeline=QuestionAnswerPipeline(rag),
    #     metricset=MetricSet(metric),
    # )
    # print(f"RAG answer correctness: {results.metrics}")
    pass


if __name__ == "__main__":
    asyncio.run(main())
