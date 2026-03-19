# Lesson 5: Putting It All Together

Time to close the loop. Remember that simple chat interface from lesson 2?
Let's upgrade it with everything we've learned:

- **RAG** for grounding answers in real documents
- **Tools** for extending what the agent can do
- **Live updates** so users see what's happening
- **UI polish** with settings and feedback

## What we're building

A chat assistant that can:
1. Answer questions using retrieved documents (RAG)
2. Use tools when needed (web search, or your custom tools)
3. Show live progress indicators when tools are running
4. Let users pick their language preference
5. Look professional with custom branding

## Core concepts

### Handling tool calls in the chat stream

When streaming agent responses, you get different types of objects:

```python
from ragbits.agents import Agent, ToolCallResult
from ragbits.core.llms import ToolCall

async for response in agent.run_streaming(input):
    match response:
        case str():
            # Regular text - show it to the user
            yield self.create_text_response(response)

        case ToolCall():
            # Agent is calling a tool - show a "working..." indicator
            yield self.create_live_update(
                response.id,
                LiveUpdateType.START,
                f"Using {response.name}...",
                "Processing your request..."
            )

        case ToolCallResult():
            # Tool finished - show completion
            yield self.create_live_update(
                response.id,
                LiveUpdateType.FINISH,
                f"{response.name} completed",
            )
```

### User settings

You can add a settings form that users fill in, and access those values
in your chat method:

```python
from ragbits.chat.interface.forms import UserSettings

class MySettings(BaseModel):
    language: Literal["English", "Polish"] = "English"

class MyChat(ChatInterface):
    user_settings = UserSettings(form=MySettings)

    async def chat(self, message, history, context):
        lang = context.user_settings.get("language", "English")
        # use lang in your prompt...
```

### Feedback forms

Collect structured feedback from users:

```python
from ragbits.chat.interface.forms import FeedbackConfig

class MyChat(ChatInterface):
    feedback_config = FeedbackConfig(
        like_enabled=True,
        like_form=LikeForm,
        dislike_enabled=True,
        dislike_form=DislikeForm,
    )
```

## Exercises

1. **[exercises/01_full_chat.py](exercises/01_full_chat.py)** - Build the complete chat with RAG, tools, and UI polish

This is the big one - it brings together everything from the workshop.
Take your time with it, and don't hesitate to look back at previous lessons.

## Running it

```bash
cd exercises
ragbits api run 01_full_chat:WorkshopChat
```

## Further reading

- [Tutorial: Chat with tools](../.ragbits/docs/tutorials/chat.md) - the full chat tutorial
- [How-To: Chat API](../.ragbits/docs/how-to/chatbots/api.md)
- [How-To: Extending chat UI](../.ragbits/docs/how-to/chatbots/extending-ui.md)
