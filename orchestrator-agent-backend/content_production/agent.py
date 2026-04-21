import os
from strands import Agent
from agents import research_agent, analyst_agent, writer_agent
from config import get_model

PORT = int(os.getenv("ORCHESTRATOR_PORT", 8000))

SYSTEM_PROMPT = """You are a content production orchestrator. You coordinate three specialists
to fulfill any content or research request.

Your workflow:
1. Use research_agent to gather facts on the topic
2. Use analyst_agent with the research output to extract key insights
3. Use writer_agent with the analysis to produce the final content

Return only the writer_agent output as your final response — do not add commentary,
summaries, or additional text around it."""


def build_agent() -> Agent:
    return Agent(
        model=get_model(),
        system_prompt=SYSTEM_PROMPT,
        tools=[research_agent, analyst_agent, writer_agent],
    )
