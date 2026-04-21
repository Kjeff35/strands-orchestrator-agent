import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from strands import tool, Agent
from config import get_model

SYSTEM_PROMPT = """You are a travel itinerary expert. Build a concise day-by-day itinerary.
- 2–3 activities per day maximum, with estimated durations
- One sentence per activity — place name, what to do, why it's worth it
- Note advance bookings on the same line
- Keep the total response under 350 words"""


@tool
def trip_planner(destination_research_and_trip_details: str) -> str:
    """Build a detailed day-by-day travel itinerary based on destination research and trip details."""
    return str(Agent(model=get_model(), system_prompt=SYSTEM_PROMPT)(destination_research_and_trip_details))
