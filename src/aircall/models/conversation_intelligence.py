"""Conversation Intelligence models for Aircall API."""
from datetime import datetime
from typing import Any, Literal, Optional

from pydantic import BaseModel

from aircall.models.participant import Participant


class Playbook(BaseModel):
    """Playbook definition object"""
    # Define based on actual API response structure


class PlaybookResultTopic(BaseModel):
    """Playbook topic result"""
    name: str
    result: Any  # Define more specifically based on API structure


class ConversationIntelligence(BaseModel):
    """
    Conversation Intelligence object for AI entities
    (Transcription, Sentiment, Topics, Summary, Action Items, Playbook Results)
    """
    id: int
    call_id: str
    call_uuid: Optional[str] = None
    number_id: Optional[int] = None
    participants: Optional[list[Participant]] = None
    type: Optional[Literal["call", "voicemail"]] = None
    content: Optional[Any] = None  # Can be string, Array, or Object
    call_created_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    created_by: Optional[int] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[int] = None
    ai_generated: Optional[bool] = None
    adherence_score: Optional[float] = None
    playbook: Optional[Playbook] = None
    playbook_result_topics: Optional[list[PlaybookResultTopic]] = None


class RealtimeTranscriptionUtterance(BaseModel):
    """Utterance object for realtime transcription webhook"""
    participant_type: Literal["internal", "external"]
    user_id: Optional[int] = None
    timestamp: int
    duration_ms: int
    text: str
    language: str


class RealtimeTranscriptionCall(BaseModel):
    """Call information for realtime transcription webhook"""
    id: Optional[int] = None
    uuid: str
    number_id: int
    direction: Literal["inbound", "outbound"]


class RealtimeTranscription(BaseModel):
    """Realtime transcription webhook event object"""
    id: str
    call: RealtimeTranscriptionCall
    utterances: list[RealtimeTranscriptionUtterance]
