import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from strands import tool, Agent
from config import get_model

SYSTEM_PROMPT = """You are a professional writer. Given analysis and insights, write polished content.
- Target 300–400 words maximum
- Strong opening sentence, logical flow, clear conclusion
- Short paragraphs, confident tone, accessible to a general technical audience"""


@tool
def writer_agent(analysis: str) -> str:
    """Write polished, engaging content from analysis and insights."""
    return str(Agent(model=get_model(), system_prompt=SYSTEM_PROMPT)(analysis))
