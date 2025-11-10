"""AI Voice Agent models for Aircall API."""
from datetime import datetime
from typing import Any, Dict, Literal, Optional

from pydantic import BaseModel


class AIVoiceAgent(BaseModel):
    """
    AI Voice Agent object representing calls handled by AI agents.

    Accessible through webhook events:
    - ai_voice_agent.started
    - ai_voice_agent.ended
    - ai_voice_agent.escalated
    - ai_voice_agent.summary

    Read-only. Not updatable or destroyable via API.
    """
    id: int  # Same value as call_id
    call_id: int  # Same value as id
    call_uuid: str
    ai_voice_agent_id: str
    ai_voice_agent_name: str
    ai_voice_agent_session_id: str
    number_id: int

    # Only for started/ended events
    external_caller_number: Optional[str] = None
    aircall_number: Optional[str] = None

    # Timestamps (Unix timestamps)
    created_at: datetime
    started_at: Optional[datetime] = None  # Only for started/ended events
    ended_at: Optional[datetime] = None  # Only for ended event

    # Only for ended event
    call_end_reason: Optional[Literal[
        "answered",
        "escalated",
        "disconnected",
        "caller_hung_up"
    ]] = None

    # Only for escalated event
    escalation_reason: Optional[str] = None

    # Only for summary event - answers to intake questions
    extracted_data: Optional[Dict[str, Any]] = None
