# Lesson 3: Retrieval-Augmented Generation (RAG)

In lesson 1, our LLM could only answer from its training data. That got us
about 68% answer correctness on a tech Q&A benchmark. Not bad, but also
not great.

The idea behind RAG is simple: before asking the LLM to answer, first
**retrieve** relevant documents and stuff them into the prompt as context.
The LLM can then base its answer on actual data instead of just vibes.

## How RAG works

```
User question
     |
     v
[1. Retrieve] -- search vector database for relevant docs
     |
     v
[2. Augment]  -- inject retrieved docs into the prompt
     |
     v
[3. Generate] -- LLM answers using the context
```

## Core concepts

### Document ingestion

Before you can search documents, you need to get them into a vector database.
The pipeline looks like this:

1. **Load** - get documents from somewhere (files, URLs, APIs)
2. **Parse** - extract text from documents (PDF, JSONL, HTML, etc.)
3. **Embed** - turn text into vector embeddings
4. **Store** - save embeddings in a vector database

Ragbits handles all of this through `DocumentSearch`:

```python
from qdrant_client import AsyncQdrantClient
from ragbits.core.embeddings import LiteLLMEmbedder
from ragbits.core.vector_stores.qdrant import QdrantVectorStore
from ragbits.document_search import DocumentSearch

retriever = DocumentSearch(
    vector_store=QdrantVectorStore(
        client=AsyncQdrantClient(path="./my_index"),  # local storage
        embedder=LiteLLMEmbedder(model_name="text-embedding-3-small"),
        index_name="my_docs",
    ),
)

# Ingest from a URL
await retriever.ingest("web://https://example.com/data.jsonl")

# Search
results = await retriever.search("how does memory management work?")
```

### Custom document parsers

If your data is in a non-standard format, you can write a custom parser:

```python
from ragbits.document_search.documents.document import Document, DocumentType
from ragbits.document_search.documents.element import Element, TextElement
from ragbits.document_search.ingestion.parsers import DocumentParser

class MyParser(DocumentParser):
    supported_document_types = {DocumentType.JSONL}

    async def parse(self, document: Document) -> list[Element]:
        # Read the file, split into elements
        ...
```

### Connecting retrieval to generation

This is where it gets interesting. We take the prompt from lesson 1,
add a `context` field, and wire up the retriever:

```python
class QuestionInput(BaseModel):
    question: str
    context: Sequence[Element] | None = None

class RAGPrompt(Prompt[QuestionInput, ReasonedAnswer]):
    system_prompt = """
    Answer the question using the provided context.
    If the context doesn't have enough info, say so.
    """
    user_prompt = """
    Question: {{ question }}
    Context: {% for chunk in context %}{{ chunk.text_representation }}{% endfor %}
    """
```

Then in your agent, search first and pass results as context:

```python
class RAGAgent(QuestionAnswerAgent):
    async def run(self, input, options=None):
        context = await retriever.search(input.question)
        return await super().run(
            QuestionInput(question=input.question, context=context)
        )
```

## Exercises

1. **[exercises/01_ingest.py](exercises/01_ingest.py)** - Ingest documents into a vector store
2. **[exercises/02_search.py](exercises/02_search.py)** - Search and inspect retrieved results
3. **[exercises/03_rag_agent.py](exercises/03_rag_agent.py)** - Build a full RAG pipeline and evaluate it

## Further reading

- [How-To: Ingest Documents](../.ragbits/docs/how-to/document_search/ingest-documents.md)
- [How-To: Search Documents](../.ragbits/docs/how-to/document_search/search-documents.md) - rephrasing, reranking, hybrid search
