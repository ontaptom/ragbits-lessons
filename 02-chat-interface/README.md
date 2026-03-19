# Lesson 2: Chat Interface

You just learned how to call an LLM and get structured responses.
Now let's put a web UI on top of it - because nobody wants to demo
things in a terminal forever.

Ragbits has a built-in `ChatInterface` that gives you a web-based chat
out of the box. The cool thing? It takes very little code.

## Core concepts

### ChatInterface - the basics

A chat interface is just a class with a `chat()` method that yields responses:

```python
from collections.abc import AsyncGenerator
from ragbits.chat.interface import ChatInterface
from ragbits.chat.interface.types import ChatContext, ChatResponse

class MyChat(ChatInterface):
    async def chat(
        self,
        message: str,
        history: list,
        context: ChatContext,
    ) -> AsyncGenerator[ChatResponse, None]:
        yield self.create_text_response("Hello! You said: " + message)
```

That's it. Seriously. Save it as `my_chat.py` and run it with:

```bash
ragbits api run my_chat:MyChat
# or with uv: uv run ragbits api run my_chat:MyChat
```

The syntax is `filename:ClassName` - so `my_chat:MyChat` means "from
`my_chat.py`, load the `MyChat` class". Same idea as `uvicorn main:app`
if you've seen that before.

And you get a full chat UI in your browser.

### Connecting it to an LLM

Of course, echoing back messages isn't very useful. Let's wire in our
LLM and prompt from the previous lesson:

```python
from ragbits.core.llms import LiteLLM
from ragbits.core.prompt import Prompt

class MyChat(ChatInterface):
    def __init__(self):
        self.llm = LiteLLM(model_name="gpt-4.1-nano")

    async def chat(self, message, history, context):
        prompt = MyPrompt(MyInput(question=message))
        response = await self.llm.generate(prompt)
        yield self.create_text_response(str(response))
```

### Streaming

For a better UX, you probably want streaming - tokens appearing as
they're generated. Ragbits supports this through agents:

```python
from ragbits.agents import Agent

class MyChat(ChatInterface):
    def __init__(self):
        self.agent = Agent(
            llm=LiteLLM(model_name="gpt-4.1-nano"),
            prompt=MyPrompt,
        )

    async def chat(self, message, history, context):
        stream = self.agent.run_streaming(MyInput(question=message))
        async for chunk in stream:
            if isinstance(chunk, str) and chunk.strip():
                yield self.create_text_response(chunk)
```

### UI customization

You can brand your chat with custom headers, welcome messages, and more:

```python
from ragbits.chat.interface.ui_customization import (
    HeaderCustomization,
    UICustomization,
)

class MyChat(ChatInterface):
    ui_customization = UICustomization(
        header=HeaderCustomization(
            title="My Workshop Bot",
            subtitle="Powered by ragbits",
        ),
        welcome_message="Hi! Ask me anything.",
        starter_questions=["What can you do?", "Tell me a joke"],
    )
```

## Exercises

1. **[exercises/01_basic_chat.py](exercises/01_basic_chat.py)** - Build a minimal chat UI backed by an LLM

## Running exercises

Unlike previous exercises, chat interfaces are started differently:

```bash
cd exercises
ragbits api run 01_basic_chat:MyChat
# or with uv: uv run ragbits api run 01_basic_chat:MyChat
```

Then open the URL shown in the terminal (usually http://127.0.0.1:8000).

## Further reading

- [How-To: Chat API](../.ragbits/docs/how-to/chatbots/api.md)
- [Tutorial: Chat](../.ragbits/docs/tutorials/chat.md) (advanced version with tools)
