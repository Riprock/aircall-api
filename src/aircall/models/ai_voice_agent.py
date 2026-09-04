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


class OutboundCallRequest(BaseModel):
    """
    An outbound call request queued for an AI Voice Agent.

    Accepted with 202; the call is queued until a concurrency slot frees up.
    Progresses through PENDING, INITIATED, IN_PROGRESS, then COMPLETED or FAILED.
    """

    id: str
    idempotency_key: Optional[str] = None
    status: Optional[Literal[
        "PENDING", "INITIATED", "IN_PROGRESS", "COMPLETED", "FAILED"
    ]] = None
    virtual_agent_id: Optional[str] = None


class CallAIVoiceAgent(BaseModel):
    """
    One AI Voice Agent segment attached to a Call.

    Returned in the call object's ai_voice_agents array when fetch_aiva_conv is
    set. A call can carry several segments when escalations are chained.
    """

    agent_id: Optional[str] = None
    agent_name: Optional[str] = None
    end_reason: Optional[str] = None
    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None
    escalation_reason: Optional[str] = None
    # {"type": "branch"|"user"|"team"|"external", "destination": ...}
    escalation_target: Optional[Dict[str, Any]] = None
