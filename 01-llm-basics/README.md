# Lesson 1: LLM Basics with Ragbits

Time to talk to a language model! In this lesson we'll learn how ragbits
wraps LLM interactions with typed prompts and structured outputs.

## Core concepts

### Prompts - not just strings

In ragbits, a prompt is a Python class. This might feel like overkill
at first, but it gives you:

- **Typed inputs** - Pydantic validates what goes into the prompt
- **Typed outputs** - you can get structured data back, not just text
- **Jinja2 templates** - flexible text formatting
- **Reusability** - prompts are testable, composable units

Here's the simplest possible prompt:

```python
from pydantic import BaseModel
from ragbits.core.prompt import Prompt

class QuestionInput(BaseModel):
    question: str

class QAPrompt(Prompt[QuestionInput, str]):
    system_prompt = """
    You are a helpful assistant. Answer questions clearly and concisely.
    """
    user_prompt = """
    Question: {{ question }}
    """
```

The `Prompt[InputType, OutputType]` generic tells ragbits what goes in
and what comes out. When `OutputType` is `str`, you get raw text back.

### Calling an LLM

Ragbits uses LiteLLM under the hood, which means you can use basically
any LLM provider with the same code:

```python
from ragbits.core.llms import LiteLLM

llm = LiteLLM(model_name="gpt-4.1-nano")  # or gemini, or anything else
prompt = QAPrompt(QuestionInput(question="What is Python?"))
response = await llm.generate(prompt)
```

### Structured output

Want more than just a string back? Define an output model:

```python
class ReasonedAnswer(BaseModel):
    reasoning: str
    answer: str

class CoTPrompt(Prompt[QuestionInput, ReasonedAnswer]):
    system_prompt = """
    You are a helpful assistant. Think step by step.
    """
    user_prompt = """
    Question: {{ question }}
    """

# Use structured output to get a parsed object back
llm = LiteLLM(model_name="gpt-4.1-nano", use_structured_output=True)
response = await llm.generate(prompt)
print(response.reasoning)  # the model's chain of thought
print(response.answer)     # the actual answer
```

### Evaluation basics

How do you know if your LLM system is any good? You measure it.
Ragbits has built-in evaluation tools:

- **DataLoader** - loads test datasets (questions + expected answers)
- **Metrics** - scores how good the output is (e.g. answer correctness)
- **Evaluator** - runs everything together with nice parallelism

We'll do a basic eval in exercise 03.

## Exercises

1. **[exercises/01_first_prompt.py](exercises/01_first_prompt.py)** - Write and run your first ragbits prompt
2. **[exercises/02_structured_output.py](exercises/02_structured_output.py)** - Get structured data back from the LLM
3. **[exercises/03_evaluation.py](exercises/03_evaluation.py)** - Evaluate your prompt against a small dataset

## Further reading

- [How-To: Prompts](../.ragbits/docs/how-to/prompts/use_prompting.md)
- [How-To: LLMs](../.ragbits/docs/how-to/llms/use_llms.md)
