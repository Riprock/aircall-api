"""Participant models for Aircall API."""
from typing import Literal

from pydantic import BaseModel


class Participant(BaseModel):
    """
    Participant in a conference call (Call Object).

    Referenced as 'conference_participants' in Call APIs
    and as 'participants' in call webhook events.
    """
    id: str | None = None  # Contact or User ID (not present for external)
    type: Literal["user", "contact", "external"]
    name: str | None = None  # Not present for external
    phone_number: str | None = None  # Not present for user type


class ConversationIntelligenceParticipant(BaseModel):
    """
    Participant in Conversation Intelligence Object.

    Used in transcription and sentiment events.
    """
    participant_type: Literal["internal", "external", "ai_voice_agent"]

    # Not present for internal or ai_voice_agent
    phone_number: str | None = None

    # Sentiment value (only for sentiment.created event)
    value: Literal["NEUTRAL", "POSITIVE", "NEGATIVE"] | None = None

    # User ID (only for transcription.created, not for external/ai_voice_agent)
    user_id: str | None = None

    # AI Voice Agent ID (only for transcription.created, only for ai_voice_agent type)
    ai_voice_agent_id: str | None = None
