# Ragbits Workshop

A hands-on introduction to [ragbits](https://ragbits.deepsense.ai/) - a Python
framework for building LLM-powered applications with RAG, agents, and chat interfaces.

## Prerequisites

- Python 3.10+
- An API key for your LLM provider (OpenAI or Google Gemini)

## Setup

Pick your package manager - either traditional pip or uv.

### Option A: Using pip

```bash
python -m venv .venv
source .venv/bin/activate

pip install -U pydantic ragbits ragbits-agents "ragbits[qdrant]"

# For the MCP exercise (lesson 04):
pip install mcp-server-fetch
```

### Option B: Using uv

[uv](https://docs.astral.sh/uv/) is a fast Python package and project manager.
If you don't have it yet:

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Then set up the project:

```bash
uv init
uv add pydantic ragbits ragbits-agents "ragbits[qdrant]"

# For the MCP exercise (lesson 04):
uv add mcp-server-fetch
```

With uv, you run scripts using `uv run` instead of `python` directly:
```bash
uv run python exercises/01_something.py
```

### API keys

```bash
export OPENAI_API_KEY="sk-..."
# or
export GEMINI_API_KEY="..."
```

Then edit `config.py` to pick your provider (OpenAI or Gemini).

## Lessons

| # | Topic | What you'll learn | Time |
|---|-------|-------------------|------|
| [00](00-python-primer/) | Python Primer | async/await, Pydantic, type hints | 15 min |
| [01](01-llm-basics/) | LLM Basics | Prompts, structured output, evaluation | 45 min |
| [02](02-chat-interface/) | Chat Interface | Web UI for your LLM in minutes | 20 min |
| [03](03-rag/) | RAG | Document ingestion, vector search, retrieval-augmented generation | 60 min |
| [04](04-agents/) | Agents & Tools | Function calling, MCP, external integrations | 45 min |
| [05](05-putting-it-together/) | Full Stack | Combine RAG + agents + chat into one app | 30 min |

## How exercises work

Each lesson folder has:
- `README.md` - theory and code examples to follow along
- `exercises/` - Python files with TODOs for you to fill in

Most exercises run with:
```bash
python exercises/01_something.py
```

Chat interface exercises run with:
```bash
ragbits api run exercises/01_something:ClassName
```

## Provider config

Edit `config.py` to switch between OpenAI and Gemini:

| Role | OpenAI | Gemini |
|------|--------|--------|
| Workhorse (cheap, fast) | `gpt-4.1-nano` | `gemini/gemini-2.5-flash-lite` |
| Smart model (eval judge, complex tasks) | `gpt-4.1` | `gemini/gemini-2.5-flash` |
| Embeddings | `text-embedding-3-small` | `gemini/text-embedding-004` |
