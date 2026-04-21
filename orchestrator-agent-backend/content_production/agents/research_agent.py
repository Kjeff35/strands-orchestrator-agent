import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from strands import tool, Agent
from strands_tools import http_request
from config import get_model

SYSTEM_PROMPT = """You are a research specialist. Given a topic, gather key facts and context.
- Search for recent, relevant information
- Focus on accuracy and concrete details
- Structure findings with clear bullet points
- Keep the total response under 300 words"""


@tool
def research_agent(query: str) -> str:
    """Research a topic in depth. Returns a detailed research brief with facts and context."""
    return str(Agent(model=get_model(), system_prompt=SYSTEM_PROMPT, tools=[http_request])(query))
