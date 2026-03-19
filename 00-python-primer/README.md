# Lesson 0: Python Primer for Java Developers

Welcome! This is a quick crash course on the Python bits you'll need
for today's workshop. We're not trying to teach all of Python here -
just the patterns that will keep popping up in ragbits code.

## Key differences from Java

### No types required (but we'll use them anyway)

Python is dynamically typed, but modern Python has **type hints** that
look a lot like Java generics. They're optional but ragbits uses them
everywhere.

```python
# No types at all - totally valid Python:
name = "hello"
names = ["a", "b"]
age = 30

# With type hints - optional but recommended:
name: str = "hello"
names: list[str] = ["a", "b"]
age: int = 30

# Java equivalent for comparison:
#   String name = "hello";
#   List<String> names = List.of("a", "b");
#   int age = 30;
```

Python won't complain if you skip type hints entirely. But ragbits uses
them everywhere, and tools like mypy can check them for you - so we'll
use them throughout the workshop.

### Pydantic - like Java records on steroids

Ragbits uses Pydantic models everywhere for data validation. Think of
them as Java records with built-in validation:

```python
from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int
    email: str | None = None  # optional field with default

user = User(name="Alice", age=30)
print(user.model_dump())  # {"name": "Alice", "age": 30, "email": None}

# This will raise a validation error - age must be int:
# User(name="Bob", age="not a number")
```

### async/await - same concept, different syntax

Java has `CompletableFuture`, Python has `async/await`. The idea is
the same - non-blocking I/O. Ragbits is async-first because LLM calls
are I/O-bound.

```python
import asyncio

async def fetch_data() -> str:
    await asyncio.sleep(1)  # simulates an API call
    return "done"

async def main() -> None:
    result = await fetch_data()
    print(result)

# This is how you run async code from a regular script:
asyncio.run(main())
```

### The `if __name__ == "__main__"` pattern

You'll see this in every exercise file. It's Python's way of saying
"only run this code if this file is executed directly" (not imported).

```python
def do_stuff():
    print("working")

if __name__ == "__main__":
    do_stuff()
```

Equivalent Java thinking: it's like having a `public static void main`
that only runs when you execute the class directly.

### Package managers and virtual environments

Python uses virtual environments to isolate project dependencies - similar
to how Maven/Gradle keep dependencies per-project in Java.

**Using pip:**
```bash
# Create a virtual environment
python -m venv .venv

# Activate it
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# Install packages (pydantic is needed for this lesson's exercises)
pip install pydantic

# Later lessons will need ragbits - you can install it now or wait:
# pip install ragbits ragbits-agents
```

**Using uv:**
```bash
# uv handles the virtual environment for you - no manual venv needed
uv init
uv add pydantic

# Later lessons will need ragbits - you can add them now or wait:
# uv add ragbits ragbits-agents
```

With uv, run scripts with `uv run python script.py` instead of just `python script.py`.

If you haven't installed uv yet, check the setup instructions in the
[main README](../README.md).

## Exercises

Work through these to get your hands dirty:

1. **[exercises/01_async.py](exercises/01_async.py)** - Practice async/await patterns
2. **[exercises/02_pydantic.py](exercises/02_pydantic.py)** - Build some Pydantic models
