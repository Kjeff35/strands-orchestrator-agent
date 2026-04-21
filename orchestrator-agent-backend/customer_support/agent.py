import os
from strands import Agent
from agents import triage_agent, faq_agent, escalation_agent
from config import get_model

PORT = int(os.getenv("ORCHESTRATOR_PORT", 8020))

SYSTEM_PROMPT = """You are a customer support orchestrator. For every customer message:

1. Use triage_agent to classify the issue, assess urgency, and extract key details
2. Use faq_agent with the triage summary to attempt resolution
3. Use escalation_agent with both the triage summary and resolution attempt to produce
   the final customer response or escalation note

Return only the escalation_agent output as your final response — do not add
commentary or restate what the other agents said."""


def build_agent() -> Agent:
    return Agent(
        model=get_model(),
        system_prompt=SYSTEM_PROMPT,
        tools=[triage_agent, faq_agent, escalation_agent],
    )
