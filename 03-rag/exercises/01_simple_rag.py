"""
Exercise: Your first RAG pipeline

Goal: Build a minimal RAG pipeline - ingest a document, search it, and
ask the LLM to answer based on the retrieved context. All in-memory,
no external databases needed.

Run:  python 01_simple_rag.py
"""

import asyncio
import sys
from collections.abc import Iterable
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))
from config import MODEL, EMBEDDING_MODEL

from pydantic import BaseModel
from ragbits.core.embeddings import LiteLLMEmbedder
from ragbits.core.llms import LiteLLM
from ragbits.core.prompt import Prompt
from ragbits.core.vector_stores import InMemoryVectorStore
from ragbits.document_search import DocumentSearch
from ragbits.document_search.documents.element import Element


# --- Step 1: Define a RAG prompt ---
# This is like the prompts from lesson 01, but with an extra `context`
# field that holds the retrieved documents.

class RAGInput(BaseModel):
    question: str
    context: Iterable[Element]


# TODO 1: Create a prompt class for RAG.
# The system prompt should tell the LLM to answer using the context.
# The user prompt should include the question AND the context chunks.
#
# class SimpleRAGPrompt(Prompt[RAGInput, str]):
#     system_prompt = """
#     You are a helpful assistant. Answer the question using the provided context.
#     If the context doesn't have enough information, say so.
#     """
#     user_prompt = """
#     Question: {{ question }}
#     Context: {% for chunk in context %}{{ chunk.text_representation }}{% endfor %}
#     """


async def main() -> None:
    llm = LiteLLM(model_name=MODEL)
    embedder = LiteLLMEmbedder(model_name=EMBEDDING_MODEL)

    # --- Step 2: Set up in-memory vector store and ingest a document ---

    # TODO 2: Create a DocumentSearch with InMemoryVectorStore and ingest a document.
    # You can use any URL - here's a classic ML paper to try:
    #
    # vector_store = InMemoryVectorStore(embedder=embedder)
    # document_search = DocumentSearch(vector_store=vector_store)
    # await document_search.ingest("web://https://arxiv.org/pdf/1706.03762")

    # --- Step 3: Search and generate ---

    # TODO 3: Search for relevant chunks and pass them to the LLM.
    #
    # question = "What is the architecture of the transformer model?"
    # chunks = await document_search.search(question)
    #
    # prompt = SimpleRAGPrompt(RAGInput(question=question, context=chunks))
    # response = await llm.generate(prompt)
    # print(response)

    # TODO 4 (bonus): Try different questions and see how the answers change.
    # Try asking something that is NOT in the document - does the LLM
    # refuse to answer as instructed?
    pass


if __name__ == "__main__":
    asyncio.run(main())
