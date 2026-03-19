"""
Exercise: Pydantic models

Ragbits uses Pydantic everywhere for structured data. Let's practice.
Fill in the TODOs and run:  python 02_pydantic.py
"""

from pydantic import BaseModel


# TODO 1: Create a Pydantic model called `Question` with:
#   - a required field `text` (str)
#   - an optional field `category` (str or None, default None)
#   - a required field `difficulty` (int)


# TODO 2: Create a model called `Answer` with:
#   - a required field `text` (str)
#   - a required field `confidence` (float) that should be between 0.0 and 1.0
#     Hint: from pydantic import Field
#     confidence: float = Field(ge=0.0, le=1.0)


# TODO 3: Create a model called `QAPair` that contains:
#   - a `question` field of type Question
#   - an `answer` field of type Answer


if __name__ == "__main__":
    # TODO 4: Create a QAPair instance and print it
    # Then try creating one with invalid data (e.g. confidence=2.0)
    # and see what happens

    # Example:
    # pair = QAPair(
    #     question=Question(text="What is Python?", difficulty=1),
    #     answer=Answer(text="A programming language", confidence=0.95),
    # )
    # print(pair.model_dump_json(indent=2))

    pass
