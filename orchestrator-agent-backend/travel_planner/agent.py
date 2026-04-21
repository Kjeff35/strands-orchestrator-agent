import os
from strands import Agent
from agents import destination_researcher, trip_planner, product_recommender
from config import get_model

PORT = int(os.getenv("ORCHESTRATOR_PORT", 8010))

SYSTEM_PROMPT = """You are a travel planning orchestrator. For any travel request:

1. Use destination_researcher to gather practical info about the destination
2. Use trip_planner with the research output plus the original trip details
3. Use product_recommender with the itinerary to suggest gear and a packing list

Return each specialist's output under a short heading. Do not rewrite, summarise, or expand
their content — present it as-is. Keep your own words to a minimum."""


def build_agent() -> Agent:
    return Agent(
        model=get_model(),
        system_prompt=SYSTEM_PROMPT,
        tools=[destination_researcher, trip_planner, product_recommender],
    )
