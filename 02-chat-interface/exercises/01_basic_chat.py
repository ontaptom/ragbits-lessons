"""
Exercise: Build a basic chat interface

Goal: Create a web-based chat UI that talks to an LLM using ragbits.

Run:  ragbits api run 01_basic_chat:MyChat
Then open http://127.0.0.1:8000 in your browser.
"""

import sys

sys.path.append("../..")
from config import MODEL

from collections.abc import AsyncGenerator

from pydantic import BaseModel
from ragbits.agents import Agent
from ragbits.chat.interface import ChatInterface
from ragbits.chat.interface.types import ChatContext, ChatResponse
from ragbits.chat.interface.ui_customization import (
    HeaderCustomization,
    UICustomization,
)
from ragbits.core.llms import LiteLLM
from ragbits.core.prompt import Prompt


# --- Step 1: Define a prompt ---

class ChatInput(BaseModel):
    question: str


# TODO 1: Create a prompt class for the chat.
# Keep it simple - a system prompt that sets the personality,
# and a user prompt that passes through the question.
#
# Some fun ideas for the system prompt:
#   - A pirate that only talks about technology
#   - A sarcastic Python teacher for Java developers
#   - A very enthusiastic hiking guide
#
# class MyChatPrompt(Prompt[ChatInput, str]):
#     system_prompt = "..."
#     user_prompt = "{{ question }}"


# --- Step 2: Build the chat interface ---

# TODO 2: Create a ChatInterface class called MyChat
#
# It should:
#   a) Have a ui_customization with a title and welcome_message
#   b) In __init__, create an Agent with your prompt and an LLM
#   c) In the chat() method, use self.agent.run_streaming() and
#      yield text responses
#
# Skeleton:
#
# class MyChat(ChatInterface):
#     ui_customization = UICustomization(
#         header=HeaderCustomization(title="My Chat", subtitle="Workshop"),
#         welcome_message="Hello! Ask me something.",
#     )
#
#     def __init__(self):
#         self.agent = Agent(
#             llm=LiteLLM(model_name=MODEL),
#             prompt=MyChatPrompt,
#         )
#
#     async def chat(
#         self,
#         message: str,
#         history: list,
#         context: ChatContext,
#     ) -> AsyncGenerator[ChatResponse, None]:
#         stream = self.agent.run_streaming(ChatInput(question=message))
#         async for chunk in stream:
#             if isinstance(chunk, str) and chunk.strip():
#                 yield self.create_text_response(chunk)
