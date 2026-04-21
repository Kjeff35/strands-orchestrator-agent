import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from strands import tool, Agent
from config import get_model

SYSTEM_PROMPT = """You are an escalation and response drafting specialist. Given a triage summary
and a resolution attempt:
- If the issue is fully resolved: draft a warm, professional closing response to send the customer
- If partially resolved: draft a response that addresses what was resolved and sets expectations for what's next
- If unresolved or high urgency: draft an escalation note for a human agent including all context,
  urgency level, and a recommended next action
- Always end with a clear next step
- Keep the total response under 200 words"""


@tool
def escalation_agent(triage_and_resolution: str) -> str:
    """Draft the final customer response or escalation note based on triage and resolution outcome."""
    return str(Agent(model=get_model(), system_prompt=SYSTEM_PROMPT)(triage_and_resolution))
