"""
Exercise: The full thing - Chat with RAG, tools, and UI polish

Goal: Build a complete chat interface that combines everything from the workshop.
This is the capstone exercise - take your time and refer back to earlier lessons.

Run:  ragbits api run 01_full_chat:WorkshopChat
Then open http://127.0.0.1:8000 in your browser.

Note: If you want RAG support, make sure you ran 03-rag/exercises/01_ingest.py first.
"""

import sys
from collections.abc import AsyncGenerator, Sequence
from typing import Literal

from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))
from config import MODEL, EMBEDDING_MODEL

from pydantic import BaseModel, ConfigDict, Field
from ragbits.agents import Agent, ToolCallResult
from ragbits.chat.interface import ChatInterface
from ragbits.chat.interface.forms import FeedbackConfig, UserSettings
from ragbits.chat.interface.types import ChatContext, ChatResponse, LiveUpdateType
from ragbits.chat.interface.ui_customization import (
    HeaderCustomization,
    PageMetaCustomization,
    UICustomization,
)
from ragbits.core.llms import LiteLLM, ToolCall
from ragbits.core.prompt import Prompt

# Uncomment these if you want RAG support (needs 03-rag/exercises/01_ingest.py run first):
# from ragbits.core.embeddings import LiteLLMEmbedder
# from ragbits.core.vector_stores import VectorStoreOptions
# from ragbits.core.vector_stores.qdrant import QdrantVectorStore
# from ragbits.document_search import DocumentSearch
# from ragbits.document_search.documents.element import Element
# from qdrant_client import AsyncQdrantClient


# ============================================================
# Part 1: Settings and feedback forms
# ============================================================

# TODO 1: Create a user settings form with a language picker.
#
# class WorkshopSettings(BaseModel):
#     model_config = ConfigDict(title="Settings", json_schema_serialization_defaults_required=True)
#     language: Literal["English", "Polish", "Spanish"] = Field(
#         description="Response language",
#         default="English",
#     )


# TODO 2 (optional): Create feedback forms for like/dislike.
#
# class LikeForm(BaseModel):
#     model_config = ConfigDict(title="Thanks!", json_schema_serialization_defaults_required=True)
#     reason: str = Field(description="What was helpful?", min_length=1)
#
# class DislikeForm(BaseModel):
#     model_config = ConfigDict(title="Feedback", json_schema_serialization_defaults_required=True)
#     issue: Literal["Incorrect", "Not helpful", "Unclear", "Other"] = Field(description="Issue type")
#     details: str = Field(description="Tell us more", min_length=1)


# ============================================================
# Part 2: Prompt and tools
# ============================================================

class ChatInput(BaseModel):
    question: str
    language: str = "English"
    # Uncomment for RAG:
    # context: Sequence[Element] | None = None


# TODO 3: Create a prompt class for the chat agent.
# Include the language variable in the system prompt.
# If using RAG, include context in the user prompt.
#
# class WorkshopPrompt(Prompt[ChatInput, str]):
#     system_prompt = """
#     You are a helpful tech assistant. Answer in {{ language }}.
#     If context is provided, base your answer on it.
#     """
#     user_prompt = """
#     {{ question }}
#     """
#     # For RAG, change user_prompt to:
#     # user_prompt = """
#     # Question: {{ question }}
#     # {% if context %}Context: {% for c in context %}{{ c.text_representation }}{% endfor %}{% endif %}
#     # """


# TODO 4 (optional): Define a custom tool for your agent.
# For example:
#
# def explain_java_in_python(java_code: str) -> str:
#     """Explain what this Java code does and show the Python equivalent."""
#     return f"Please explain this Java code and show the Python version:\n{java_code}"


# ============================================================
# Part 3: The chat interface
# ============================================================

# TODO 5: Build the chat interface class.
# This pulls together everything from the workshop.
#
# class WorkshopChat(ChatInterface):
#     ui_customization = UICustomization(
#         header=HeaderCustomization(
#             title="Workshop Assistant",
#             subtitle="Ragbits workshop",
#         ),
#         welcome_message=(
#             "Welcome to the ragbits workshop chat!\n\n"
#             "Try asking me tech questions. I can search through documents "
#             "and use tools to help you."
#         ),
#         starter_questions=[
#             "What is RAG and why is it useful?",
#             "Explain async/await in Python",
#             "What are vector embeddings?",
#         ],
#         meta=PageMetaCustomization(page_title="Workshop Chat"),
#     )
#
#     # Uncomment to add settings and feedback:
#     # user_settings = UserSettings(form=WorkshopSettings)
#     # feedback_config = FeedbackConfig(
#     #     like_enabled=True, like_form=LikeForm,
#     #     dislike_enabled=True, dislike_form=DislikeForm,
#     # )
#     # conversation_history = True
#
#     def __init__(self):
#         self.llm = LiteLLM(model_name=MODEL)
#
#         # Uncomment for RAG:
#         # self.retriever = DocumentSearch(
#         #     vector_store=QdrantVectorStore(
#         #         client=AsyncQdrantClient(path="../../../03-rag/exercises/ragqa_arena_tech_corpus"),
#         #         embedder=LiteLLMEmbedder(model_name=EMBEDDING_MODEL),
#         #         default_options=VectorStoreOptions(k=5),
#         #         index_name="ragqa_arena_tech_corpus",
#         #     ),
#         # )
#
#         self.agent = Agent(
#             llm=self.llm,
#             prompt=WorkshopPrompt,
#             tools=[],  # add your tools here
#         )
#
#     async def chat(
#         self,
#         message: str,
#         history: list,
#         context: ChatContext,
#     ) -> AsyncGenerator[ChatResponse, None]:
#         # Get language from settings (if you set up WorkshopSettings)
#         language = "English"
#         # if context and context.user_settings:
#         #     language = context.user_settings.get("language", "English")
#
#         # Optional: retrieve context for RAG
#         # search_results = await self.retriever.search(message)
#
#         # Build input
#         chat_input = ChatInput(
#             question=message,
#             language=language,
#             # context=search_results,  # uncomment for RAG
#         )
#
#         # Stream the response
#         stream = self.agent.run_streaming(chat_input)
#         async for response in stream:
#             match response:
#                 case str():
#                     if response.strip():
#                         yield self.create_text_response(response)
#                 case ToolCall():
#                     yield self.create_live_update(
#                         response.id,
#                         LiveUpdateType.START,
#                         f"Using {response.name}...",
#                         "Working on it...",
#                     )
#                 case ToolCallResult():
#                     yield self.create_live_update(
#                         response.id,
#                         LiveUpdateType.FINISH,
#                         f"{response.name} done",
#                     )
