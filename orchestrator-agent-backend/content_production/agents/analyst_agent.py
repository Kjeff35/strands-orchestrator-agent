import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from strands import tool, Agent
from config import get_model

SYSTEM_PROMPT = """You are an analysis specialist. Given research material, return a concise analysis.
- Extract the 3–4 most significant insights only
- State each insight in 1–2 sentences
- Keep the total response under 200 words"""


@tool
def analyst_agent(research_brief: str) -> str:
    """Analyse research findings and extract key insights, themes, and conclusions."""
    return str(Agent(model=get_model(), system_prompt=SYSTEM_PROMPT)(research_brief))
