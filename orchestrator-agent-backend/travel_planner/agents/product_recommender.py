import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from strands import tool, Agent
from config import get_model

SYSTEM_PROMPT = """You are a travel gear and packing expert. Return a concise packing list.
- Clothing: 4–5 items maximum
- Gear and accessories: 4–5 items maximum
- One commonly forgotten item to flag
- Keep the total response under 200 words"""


@tool
def product_recommender(itinerary_and_trip_details: str) -> str:
    """Recommend travel gear, clothing, and a packing list tailored to the itinerary."""
    return str(Agent(model=get_model(), system_prompt=SYSTEM_PROMPT)(itinerary_and_trip_details))
