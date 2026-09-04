"""Conversation Intelligence models for Aircall API."""
from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel

from aircall.models.participant import Participant


class Playbook(BaseModel):
    """
    Playbook definition.

    Included in a playbook result only when fetch_playbook=true is passed to
    CallResource.get_playbook_result().
    """
    id: int | None = None
    name: str | None = None
    language: str | None = None


class PlaybookResultTopic(BaseModel):
    """One topic's result within a playbook result"""
    name: str
    # Documented only as placeholder "content"; left permissive rather than
    # guessing a type Aircall has not specified.
    result: Any = None


class ConversationIntelligence(BaseModel):
    """
    Conversation Intelligence object for AI entities
    (Transcription, Sentiment, Topics, Summary, Action Items, Playbook Results)
    """
    id: int
    call_id: str
    call_uuid: str | None = None
    number_id: int | None = None
    participants: list[Participant] | None = None
    type: Literal["call", "voicemail"] | None = None
    content: Any | None = None  # Can be string, Array, or Object
    call_created_at: datetime | None = None
    created_at: datetime | None = None
    created_by: int | None = None
    updated_at: datetime | None = None
    updated_by: int | None = None
    ai_generated: bool | None = None
    adherence_score: float | None = None
    playbook: Playbook | None = None
    playbook_result_topics: list[PlaybookResultTopic] | None = None


class RealtimeTranscriptionUtterance(BaseModel):
    """Utterance object for realtime transcription webhook"""
    participant_type: Literal["internal", "external"]
    user_id: int | None = None
    timestamp: int
    duration_ms: int
    text: str
    language: str


class RealtimeTranscriptionCall(BaseModel):
    """Call information for realtime transcription webhook"""
    id: int | None = None
    uuid: str
    number_id: int
    direction: Literal["inbound", "outbound"]


class RealtimeTranscription(BaseModel):
    """Realtime transcription webhook event object"""
    id: str
    call: RealtimeTranscriptionCall
    utterances: list[RealtimeTranscriptionUtterance]
