"""
Exercise: Build a basic chat interface

Goal: Create a web-based chat UI that talks to an LLM using ragbits.

Run:  ragbits api run 01_basic_chat:MyChat
Then open http://127.0.0.1:8000 in your browser.
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))
from config import MODEL

from collections.abc import AsyncGenerator

from pydantic import BaseModel
from ragbits.chat.interface import ChatInterface
from ragbits.chat.interface.types import ChatContext, ChatResponse
from ragbits.core.prompt import ChatFormat
from ragbits.chat.interface.ui_customization import (
    HeaderCustomization,
    UICustomization,
)
from ragbits.core.llms import LiteLLM
from ragbits.core.prompt import Prompt


# TODO 1: Build a ChatInterface class called MyChat.
#
# You need:
#   a) A prompt class (same pattern as lesson 01 - input model, system prompt, user prompt)
#   b) A ChatInterface subclass that creates an LLM in __init__,
#      and in chat() generates a response and yields it
#   c) UI customization with a title and welcome message
#
# Pick a fun personality for your system prompt:
#   - A pirate that only talks about technology
#   - A sarcastic Python teacher for Java developers
#   - A very enthusiastic hiking guide
#
# Skeleton:
#
# class ChatInput(BaseModel):
#     question: str
#
# class MyChatPrompt(Prompt[ChatInput, str]):
#     system_prompt = "..."
#     user_prompt = "{{ question }}"
#
# class MyChat(ChatInterface):
#     ui_customization = UICustomization(
#         header=HeaderCustomization(title="My Chat", subtitle="Workshop"),
#         welcome_message="Hello! Ask me something.",
#     )
#
#     def __init__(self):
#         self.llm = LiteLLM(model_name=MODEL)
#
#     async def chat(
#         self,
#         message: str,
#         history: ChatFormat,
#         context: ChatContext,
#     ) -> AsyncGenerator[ChatResponse, None]:
#         prompt = MyChatPrompt(ChatInput(question=message))
#         response = await self.llm.generate(prompt)
#         yield self.create_text_response(str(response))


# TODO 2 (bonus): Once it works, try upgrading to streaming responses.
# You'll need Agent from ragbits.agents:
#
#   from ragbits.agents import Agent
#
#   self.agent = Agent(llm=LiteLLM(model_name=MODEL), prompt=MyChatPrompt)
#
# Then in chat(), replace llm.generate with:
#
#   stream = self.agent.run_streaming(ChatInput(question=message))
#   async for chunk in stream:
#       if isinstance(chunk, str) and chunk.strip():
#           yield self.create_text_response(chunk)
