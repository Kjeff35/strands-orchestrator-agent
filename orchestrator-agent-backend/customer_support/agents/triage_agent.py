import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from strands import tool, Agent
from config import get_model

SYSTEM_PROMPT = """You are a customer support triage specialist. Given a customer message:
- Identify the issue category: billing, technical, general enquiry, or complaint
- Assess urgency: low / medium / high
- Extract key details: account info mentioned, product involved, what the customer wants
- Output a structured triage summary that the next agent can act on immediately
- Do NOT attempt to resolve the issue yourself
- Keep the total response under 150 words"""


@tool
def triage_agent(customer_message: str) -> str:
    """Triage a customer message: classify issue type, urgency, and extract key details."""
    return str(Agent(model=get_model(), system_prompt=SYSTEM_PROMPT)(customer_message))
