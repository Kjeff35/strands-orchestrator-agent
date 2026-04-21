import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from strands import tool, Agent
from strands_tools import http_request
from config import get_model

SYSTEM_PROMPT = """You are a destination research specialist. Return a concise destination brief.
- Visa requirements: 1–2 sentences
- Climate and best time to visit: 1–2 sentences
- Safety and key local laws: 1–2 sentences
- Cultural norms and language basics: 1–2 sentences
- Currency and rough costs: 1–2 sentences
Keep the total response under 250 words."""


@tool
def destination_researcher(destination_and_context: str) -> str:
    """Research practical destination details: visa, climate, safety, culture, and costs."""
    return str(Agent(model=get_model(), system_prompt=SYSTEM_PROMPT, tools=[http_request])(destination_and_context))
