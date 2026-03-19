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
Ragbits has a built-in evaluation framework with a few moving parts.
Let's walk through them.

#### QuestionAnswerAgent - a thin wrapper

Before we can evaluate, we need something that takes a question and
returns an answer. Ragbits provides `QuestionAnswerAgent` for exactly
this - it's a lightweight agent that wraps an LLM + prompt into a
callable unit. Don't worry about the "agent" part yet - we'll dig
into agents properly in lesson 04. For now, think of it as a
convenience class:

```python
from ragbits.agents.types import QuestionAnswerAgent

agent = QuestionAnswerAgent(llm=llm, prompt=QAPrompt)
result = await agent.run(QuestionInput(question="What is Python?"))
print(result.content)  # the answer (typed by your output model)
```

#### DataLoader - loading test data

You need a dataset of questions with expected answers to evaluate against.
`QuestionAnswerDataLoader` loads one from a URL or file:

```python
from ragbits.core.sources import WebSource
from ragbits.evaluate.dataloaders.question_answer import QuestionAnswerDataLoader

dataloader = QuestionAnswerDataLoader(
    source=WebSource(url="https://example.com/qa_dataset.jsonl"),
    split="data[:20]",       # just 20 examples to keep it quick
    question_key="question",  # which JSON field has the question
    answer_key="response",    # which JSON field has the expected answer
)
dataset = await dataloader.load()
```

#### Metrics - scoring the output

A metric takes your agent's answers and scores them. The judge is
typically a smarter model than the one generating answers:

```python
from ragbits.evaluate.metrics.question_answer import QuestionAnswerAnswerCorrectness

judge = LiteLLM(model_name="gpt-4.1")  # smarter model as judge
metric = QuestionAnswerAnswerCorrectness(judge)
```

#### Evaluator - putting it all together

The `Evaluator` wires everything up - it feeds data through a pipeline,
collects results, and computes metrics:

```python
from ragbits.evaluate.evaluator import Evaluator
from ragbits.evaluate.metrics import MetricSet
from ragbits.evaluate.pipelines.question_answer import QuestionAnswerPipeline

evaluator = Evaluator()
results = await evaluator.compute(
    dataloader=dataloader,
    pipeline=QuestionAnswerPipeline(agent),
    metricset=MetricSet(metric),
)
print(results.metrics)  # e.g. {'LLM_based_answer_correctness': 0.68}
```

We'll do exactly this in exercise 03.

## Exercises

1. **[exercises/01_first_prompt.py](exercises/01_first_prompt.py)** - Write and run your first ragbits prompt
2. **[exercises/02_structured_output.py](exercises/02_structured_output.py)** - Get structured data back from the LLM
3. **[exercises/03_evaluation.py](exercises/03_evaluation.py)** - Evaluate your prompt against a small dataset
4. **[exercises/04_cli_chat.py](exercises/04_cli_chat.py)** - Build a terminal chatbot (teaser for lesson 02)

## Further reading

- [How-To: Prompts](../.ragbits/docs/how-to/prompts/use_prompting.md)
- [How-To: LLMs](../.ragbits/docs/how-to/llms/use_llms.md)
