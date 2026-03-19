"""
Exercise: Ingest documents into a vector store

Goal: Download a corpus of tech documents and index them for search.

Run:  python 01_ingest.py

This will create a local Qdrant database in ./ragqa_arena_tech_corpus/
The ingestion takes about 2 minutes - grab a coffee.
"""

import asyncio
import json
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))
from config import EMBEDDING_MODEL

from ragbits.core.embeddings import LiteLLMEmbedder
from ragbits.core.vector_stores import VectorStoreOptions
from ragbits.document_search import DocumentSearch
from ragbits.document_search.documents.document import Document, DocumentType
from ragbits.document_search.documents.element import Element, TextElement
from ragbits.document_search.ingestion.parsers import DocumentParser, DocumentParserRouter
from ragbits.document_search.ingestion.strategies import BatchedIngestStrategy

# We need qdrant for the vector store
from qdrant_client import AsyncQdrantClient
from ragbits.core.vector_stores.qdrant import QdrantVectorStore


# --- Step 1: Custom document parser ---
# The corpus is in JSONL format (one JSON object per line, each with a "text" field).
# We need to tell ragbits how to parse this.

MAX_CHARACTERS = 6000  # truncate very long documents

class RAGQADocumentParser(DocumentParser):
    supported_document_types = {DocumentType.JSONL}

    async def parse(self, document: Document) -> list[Element]:
        return [
            TextElement(
                content=parsed["text"][:MAX_CHARACTERS],
                document_meta=document.metadata,
            )
            for line in document.local_path.read_text().strip().split("\n")
            if (parsed := json.loads(line))
        ]


# --- Step 2: Configure the retriever ---

# TODO 1: Create a DocumentSearch instance with:
#   - QdrantVectorStore using a local path "./ragqa_arena_tech_corpus"
#   - LiteLLMEmbedder with EMBEDDING_MODEL
#   - VectorStoreOptions(k=5) for top-5 retrieval
#   - BatchedIngestStrategy for efficient bulk ingestion
#   - DocumentParserRouter mapping JSONL to our custom parser
#
# retriever = DocumentSearch(
#     vector_store=QdrantVectorStore(
#         client=AsyncQdrantClient(path="./ragqa_arena_tech_corpus"),
#         embedder=LiteLLMEmbedder(model_name=EMBEDDING_MODEL),
#         default_options=VectorStoreOptions(k=5),
#         index_name="ragqa_arena_tech_corpus",
#     ),
#     ingest_strategy=BatchedIngestStrategy(index_batch_size=1000),
#     parser_router=DocumentParserRouter({DocumentType.JSONL: RAGQADocumentParser()}),
# )


async def main() -> None:
    # TODO 2: Ingest the corpus from this URL:
    # "web://https://huggingface.co/datasets/deepsense-ai/ragbits/resolve/main/ragqa_arena_tech_corpus.jsonl"
    #
    # results = await retriever.ingest("web://...")
    # print(results)

    print("Done! The index is saved in ./ragqa_arena_tech_corpus/")
    print("You can now run 02_search.py to query it.")


if __name__ == "__main__":
    asyncio.run(main())
