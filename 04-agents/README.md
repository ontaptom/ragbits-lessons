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
    """
    Returns the current weather for a given city.

    Args:
        city: The city to get the weather for.
    """
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
Instead of writing tool functions yourself, you connect to a server that
already provides them. Your agent discovers what tools are available and
calls them as needed.

Ragbits supports three MCP transports:

#### 1. Stdio - local child process

The server runs as a subprocess of your application. Simplest to set up,
great for development. You need to install the server package first:

```bash
pip install mcp-server-fetch
# or with uv: uv add mcp-server-fetch
```

```python
from ragbits.agents.mcp import MCPServerStdio

server = MCPServerStdio(params={"command": "python", "args": ["-m", "mcp_server_fetch"]})
```

#### 2. SSE - remote server over Server-Sent Events

Connect to an MCP server running somewhere on the network. This is the
older remote transport - still widely used:

```python
from ragbits.agents.mcp import MCPServerSse

server = MCPServerSse(params={"url": "http://localhost:8080/sse"})
```

#### 3. Streamable HTTP - the newer remote transport

The recommended transport for remote MCP servers. Same idea as SSE but
uses standard HTTP:

```python
from ragbits.agents.mcp import MCPServerStreamableHttp

server = MCPServerStreamableHttp(params={"url": "https://mcp.deepwiki.com/mcp"})
```

In production, MCP servers are usually separate, independently running
services (their own containers, processes, etc.) - not child processes.
For local development and workshops, `MCPServerStdio` is the quickest
way to get started. For remote servers, prefer Streamable HTTP.

#### Context managers and `async with`

All three transports need to be opened before use and closed after.
Python has a pattern for this called **context managers** - the
`with` / `async with` block. You've probably seen it with files:

```python
with open("file.txt") as f:
    data = f.read()
# file is automatically closed here, even if an exception was thrown
```

If you're coming from Java, this is the same idea as try-with-resources
and `AutoCloseable`. The `async with` variant works the same way but
for async code:

```python
async with server:
    agent = Agent(
        llm=llm,
        prompt=MyPrompt,
        mcp_servers=[server],
    )
    result = await agent.run(MyInput(question="Summarize https://example.com"))
    print(result.content)
# connection is automatically closed here
```

For stdio, `async with` starts and stops the child process.
For SSE and HTTP, it opens and closes the network connection.

### A2A - agents talking to agents (overview)

The Agent-to-Agent (A2A) protocol lets you expose ragbits agents as HTTP
services. Other agents (or any HTTP client) can discover and call them.

This is more of an advanced topic - we'll just cover the concept here.
The idea is that you can build specialized agents (flight search, city info,
weather) and have an orchestrator agent coordinate between them.

## Exercises

1. **[exercises/01_tool_calling.py](exercises/01_tool_calling.py)** - Build an agent with custom tools
2. **[exercises/02_mcp_agent.py](exercises/02_mcp_agent.py)** - Use MCP to give your agent web browsing (local stdio server)
3. **[exercises/03_external_mcp_agent.py](exercises/03_external_mcp_agent.py)** - Connect to a remote MCP server over HTTP (no install needed)

## Further reading

- [How-To: Define and use agents](../.ragbits/docs/how-to/agents/define_and_use_agents.md)
- [How-To: Tool calling](../.ragbits/docs/how-to/llms/use_tools_with_llms.md)
- [How-To: MCP tools](../.ragbits/docs/how-to/agents/provide_mcp_tools.md)
- [Tutorial: Multi-agent with A2A](../.ragbits/docs/tutorials/agents.md)
