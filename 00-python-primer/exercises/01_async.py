"""
Exercise: async/await basics

In this exercise you'll practice the async patterns used throughout ragbits.
Fill in the TODOs and run:  python 01_async.py
"""

import asyncio
import random


# TODO 1: Make this function async and have it return "Hello, {name}!"
# Hint: add the `async` keyword before `def`
async def greet(name: str) -> str:
    print(f"Hello, {name}!")
    delay = random.randint(1, 5)
    await asyncio.sleep(delay)
    return f"Nice to see you, {name}! (took {delay}s)"


# TODO 2: Write an async function called `greet_many` that takes a list of names,
# calls `greet()` for each one (with await), and returns a list of greetings.
# Hint: you can use asyncio.gather() to run them concurrently, or just loop.

# option B - sequential: one at a time, total time = sum of all delays
async def greet_many(names: list[str]) -> list[str]:
    results = []
    for name in names:
        results.append(await greet(name))
    return results

# option A - concurrent: all greetings start at once, total time = slowest one
async def greet_many(names: list[str]) -> list[str]:
    return await asyncio.gather(*[greet(name) for name in names])

# option C - concurrent with create_task: schedule tasks explicitly, then await
async def greet_many(names: list[str]) -> list[str]:
    tasks = [asyncio.create_task(greet(name)) for name in names]
    return [await task for task in tasks]


# TODO 3: Write an async `main()` that:
#   - calls greet("World") and prints the result
#   - calls greet_many(["Alice", "Bob", "Charlie"]) and prints all results
async def main() -> None:
    result = await greet("World")
    print(result)

    results = await greet_many(["Alice", "Bob", "Charlie"])
    print(results)


if __name__ == "__main__":
    # TODO 4: Run the main() function using asyncio.run()
    asyncio.run(main())
