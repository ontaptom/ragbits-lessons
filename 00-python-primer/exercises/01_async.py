"""
Exercise: async/await basics

In this exercise you'll practice the async patterns used throughout ragbits.
Fill in the TODOs and run:  python 01_async.py
"""

import asyncio


# TODO 1: Make this function async and have it return "Hello, {name}!"
# Hint: add the `async` keyword before `def`
def greet(name: str) -> str:
    return f"Hello, {name}!"


# TODO 2: Write an async function called `greet_many` that takes a list of names,
# calls `greet()` for each one (with await), and returns a list of greetings.
# Hint: you can use asyncio.gather() to run them concurrently, or just loop.


# TODO 3: Write an async `main()` that:
#   - calls greet("World") and prints the result
#   - calls greet_many(["Alice", "Bob", "Charlie"]) and prints all results


if __name__ == "__main__":
    # TODO 4: Run the main() function using asyncio.run()
    pass
