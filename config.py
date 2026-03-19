"""
Workshop configuration - pick your LLM provider here.

Uncomment the provider you want to use and make sure
you have the corresponding API key set in your environment:
  - OpenAI:  export OPENAI_API_KEY="sk-..."
  - Gemini:  export GEMINI_API_KEY="..."
"""

# --- Option A: OpenAI (default) ---
MODEL = "gpt-4.1-nano"
MODEL_SMART = "gpt-4.1"
EMBEDDING_MODEL = "text-embedding-3-small"

# --- Option B: Google Gemini ---
# MODEL = "gemini/gemini-2.5-flash-lite"
# MODEL_SMART = "gemini/gemini-2.5-flash"
# EMBEDDING_MODEL = "gemini/text-embedding-004"
