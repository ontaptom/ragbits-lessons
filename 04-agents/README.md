# Lesson 4: Agents and Tools

So far our LLM can answer questions and use retrieved documents. But what
if you want it to actually *do* things - call APIs, look up data, run
calculations?

That's where agents come in. An agent is an LLM that can decide to call
**tools** (Python functions) based on the conversation. The LLM looks at
the available tools, decides which one to call, and ragbits handles the
execution and feeds results back.

## Core concepts

### Tool calling - how it works

1. You define Python functions and register them as tools
2. The LLM sees the function names, descriptions, and parameter schemas
3. When a user asks something, the LLM can decide to call a tool
4. Ragbits executes the function and sends results back to the LLM
5. The LLM uses the results to formulate its answer

```
User: "What's the weather in Paris?"
  |
  v
LLM thinks: "I should call get_weather(city='Paris')"
  |
  v
Ragbits runs: get_weather(city="Paris") -> "15C, cloudy"
  |
  v
LLM: "The weather in Paris is 15C and cloudy."
```

### Defining tools

A tool is just a Python function with type hints and a docstring:

```python
def get_weather(city: str) -> str:
    """Get current weather for a city."""
    # In real life, call a weather API here
    return f"Weather in {city}: 15C, partly cloudy"
```

### Creating an agent

```python
from ragbits.agents import Agent
from ragbits.core.llms import LiteLLM

agent = Agent(
    llm=LiteLLM(model_name="gpt-4.1-nano"),
    prompt=MyPrompt,
    tools=[get_weather],
)

result = await agent.run(MyInput(question="What's the weather in Paris?"))
```

### MCP - reuse tools without writing code

The Model Context Protocol (MCP) lets you plug in existing tool servers.
For example, there's an `mcp-server-fetch` that gives your agent the
ability to fetch and read web pages - no code needed:

```bash
pip install mcp-server-fetch
# or with uv: uv add mcp-server-fetch
```

```python
from ragbits.agents.mcp import MCPServerStdio

agent = Agent(
    llm=llm,
    prompt=MyPrompt,
    mcp_servers=[
        MCPServerStdio(command="python", args=["-m", "mcp_server_fetch"]),
    ],
)
```

The agent now has a `fetch` tool it can use to read any URL. You didn't
write a single line of tool code.

### A2A - agents talking to agents (overview)

The Agent-to-Agent (A2A) protocol lets you expose ragbits agents as HTTP
services. Other agents (or any HTTP client) can discover and call them.

This is more of an advanced topic - we'll just cover the concept here.
The idea is that you can build specialized agents (flight search, city info,
weather) and have an orchestrator agent coordinate between them.

## Exercises

1. **[exercises/01_tool_calling.py](exercises/01_tool_calling.py)** - Build an agent with custom tools
2. **[exercises/02_mcp_agent.py](exercises/02_mcp_agent.py)** - Use MCP to give your agent web browsing

## Further reading

- [How-To: Define and use agents](../.ragbits/docs/how-to/agents/define_and_use_agents.md)
- [How-To: Tool calling](../.ragbits/docs/how-to/llms/use_tools_with_llms.md)
- [How-To: MCP tools](../.ragbits/docs/how-to/agents/provide_mcp_tools.md)
- [Tutorial: Multi-agent with A2A](../.ragbits/docs/tutorials/agents.md)
