import logging
from typing import Dict

from bedrock_agentcore import BedrockAgentCoreApp
from starlette.middleware.cors import CORSMiddleware
from strands import Agent

from agent import build_agent, PORT

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("travel-planner")

app = BedrockAgentCoreApp()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

_sessions: dict[str, Agent] = {}


def get_or_create_agent(session_id: str, actor_id: str) -> Agent:
    key = f"{actor_id}:{session_id}"
    if key not in _sessions:
        logger.info("Creating new agent session: %s", key)
        _sessions[key] = build_agent()
    else:
        logger.info("Reusing existing agent session: %s", key)
    return _sessions[key]


@app.entrypoint
async def invoke_stream(payload: Dict, _context=None):
    """Streaming AgentCore entrypoint for the travel planner orchestrator."""

    user_id = payload.get("user_id")
    if not user_id or not isinstance(user_id, str) or not user_id.strip():
        logger.warning("Request rejected: missing user_id")
        yield {"error": "Authentication required: 'user_id' must be provided and non-empty", "code": "missing_user_id"}
        return
    actor_id = user_id.strip()

    session_id = payload.get("session_id")
    if not session_id or not isinstance(session_id, str) or not session_id.strip():
        logger.warning("Request rejected: missing session_id for user %s", actor_id)
        yield {"error": "'session_id' must be provided and non-empty", "code": "missing_session_id"}
        return

    user_message = payload.get("prompt") or payload.get("message") or payload.get("question", "")
    if not user_message:
        logger.warning("Request rejected: no message provided")
        yield {"error": "No prompt, message, or question provided"}
        return

    logger.info("Invoking agent | user=%s session=%s message=%r", actor_id, session_id, user_message[:80])
    agent = get_or_create_agent(session_id, actor_id)

    try:
        async for event in agent.stream_async(user_message):
            if not isinstance(event, dict) or "event" not in event:
                continue
            bedrock_event = event["event"]
            if "toolUse" in bedrock_event.get("contentBlockDelta", {}).get("delta", {}):
                continue
            tool_name = (
                bedrock_event
                .get("contentBlockStart", {})
                .get("start", {})
                .get("toolUse", {})
                .get("name")
            )
            if tool_name:
                logger.info("Tool call → %s", tool_name)
                yield {"tool_use": {"name": tool_name}}
            yield event
        logger.info("Stream complete | session=%s", session_id)
    except Exception as e:
        logger.exception("Streaming failed: %s", e)
        yield {"error": f"Streaming failed: {str(e)}"}


if __name__ == "__main__":
    logger.info("Starting travel-planner agent on port %d", PORT)
    app.run(host="0.0.0.0", port=PORT)
