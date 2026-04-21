import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from strands import tool, Agent
from config import get_model

SYSTEM_PROMPT = """You are a customer support resolution specialist. Given a triage summary:
- For billing issues: explain charges, refund policies, and payment options clearly
- For technical issues: provide step-by-step troubleshooting instructions
- For general enquiries: answer directly and completely
- Keep responses friendly, concise, and actionable
- If you cannot resolve it fully, clearly state what is unresolved for escalation
- Keep the total response under 200 words"""


@tool
def faq_agent(triage_summary: str) -> str:
    """Resolve customer issues using knowledge of billing, technical support, and FAQs."""
    return str(Agent(model=get_model(), system_prompt=SYSTEM_PROMPT)(triage_summary))
