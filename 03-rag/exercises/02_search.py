"""
Exercise: Search the vector store

Goal: Query the index we built in 01_ingest.py and inspect the results.
Make sure you ran 01_ingest.py first!

Run:  python 02_search.py
"""

import asyncio
import sys

sys.path.append("../..")
from config import EMBEDDING_MODEL

from ragbits.core.embeddings import LiteLLMEmbedder
from ragbits.core.vector_stores import VectorStoreOptions
from ragbits.core.vector_stores.qdrant import QdrantVectorStore
from ragbits.document_search import DocumentSearch

from qdrant_client import AsyncQdrantClient


# --- Reconnect to the index we built in 01_ingest.py ---

retriever = DocumentSearch(
    vector_store=QdrantVectorStore(
        client=AsyncQdrantClient(path="./ragqa_arena_tech_corpus"),
        embedder=LiteLLMEmbedder(model_name=EMBEDDING_MODEL),
        default_options=VectorStoreOptions(k=5),
        index_name="ragqa_arena_tech_corpus",
    ),
)


async def main() -> None:
    # TODO 1: Search for something and print the results.
    # Try different queries and see what comes back.
    #
    # results = await retriever.search("What are high memory and low memory on linux?")
    # for i, result in enumerate(results):
    #     print(f"\n--- Result {i+1} ---")
    #     print(result.text_representation[:300])

    # TODO 2: Try a few more queries. Some ideas:
    #   - "how does TCP handshake work?"
    #   - "what is docker compose?"
    #   - "explain kubernetes pods"
    # Do the results make sense? Are they relevant?

    # TODO 3 (bonus): Try changing VectorStoreOptions(k=...) in the retriever
    # above to get more or fewer results. What's a good number?
    pass


if __name__ == "__main__":
    asyncio.run(main())
