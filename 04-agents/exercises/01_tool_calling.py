"""
Exercise: Build an agent with custom tools

Goal: Create an agent that can use Python functions to answer questions.
The LLM will decide when to call your tools based on the user's question.

Run:  python 01_tool_calling.py
"""

import asyncio
import json
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))
from config import MODEL

from pydantic import BaseModel
from ragbits.agents import Agent
from ragbits.core.llms import LiteLLM
from ragbits.core.prompt import Prompt


# --- Step 1: Define some tools ---

# Here's an example tool. In a real app this would call an actual API.

def search_flights(departure: str, destination: str) -> str:
    """Search for available flights between two cities."""
    # Fake flight data - in production you'd call a flight API
    flights = {
        ("new york", "paris"): [
            {"airline": "Air France", "departure": "10:00", "arrival": "22:00", "price": "$450"},
            {"airline": "Delta", "departure": "13:00", "arrival": "01:00", "price": "$520"},
        ],
        ("london", "tokyo"): [
            {"airline": "JAL", "departure": "11:00", "arrival": "07:00+1", "price": "$890"},
        ],
    }
    key = (departure.lower(), destination.lower())
    results = flights.get(key, [])
    if not results:
        return f"No flights found from {departure} to {destination}"
    return json.dumps(results, indent=2)


# TODO 1: Write your own tool function. Some ideas:
#   - get_weather(city: str) -> str
#   - convert_currency(amount: float, from_currency: str, to_currency: str) -> str
#   - get_hotel_prices(city: str, checkin: str, checkout: str) -> str
#
# Remember: the function needs type hints and a docstring.
# The docstring is what the LLM reads to understand what the tool does.


# --- Step 2: Define the prompt ---

class TravelInput(BaseModel):
    question: str


# TODO 2: Create a prompt for a travel assistant agent.
# The system prompt should mention that the agent has access to tools.
#
# class TravelPrompt(Prompt[TravelInput, str]):
#     system_prompt = """
#     You are a helpful travel assistant. You have access to tools
#     that can search for flights and other travel information.
#     Use them when the user asks about travel plans.
#     """
#     user_prompt = "{{ question }}"


async def main() -> None:
    # --- Step 3: Create the agent ---

    # TODO 3: Create an Agent with your tools.
    # agent = Agent(
    #     llm=LiteLLM(model_name=MODEL),
    #     prompt=TravelPrompt,
    #     tools=[search_flights],  # add your custom tool here too!
    # )

    # TODO 4: Test it! Ask questions that require tool use.
    # result = await agent.run(TravelInput(question="Find me flights from New York to Paris"))
    # print(result.content)

    # TODO 5: Ask something that requires your custom tool.
    # Also try asking something that doesn't need any tool - the agent
    # should just answer normally.
    pass


if __name__ == "__main__":
    asyncio.run(main())
