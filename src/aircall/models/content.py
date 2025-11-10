"""Content models for Aircall API."""
from typing import Literal, Optional

from pydantic import BaseModel


class Utterance(BaseModel):
    """A single sentence/utterance in a transcription"""
    start_time: float
    end_time: float
    text: str
    participant_type: Literal["external", "internal"]
    user_id: Optional[int] = None
    phone_number: Optional[str] = None


class Content(BaseModel):
    """Content object for transcription type"""
    language: Literal[
        "en", "en-US", "en-GB", "en-AU",
        "fr-FR", "fr",
        "es-ES", "es",
        "de-DE", "de",
        "nl-NL", "nl",
        "it-IT", "it"
    ]
    utterances: list[Utterance] = []


class SummaryContent(BaseModel):
    """Content object for summary type"""
    content: str


class TopicsContent(BaseModel):
    """Content object for topics type"""
    content: list[str] = []


class ActionItemsContent(BaseModel):
    """Content object for action items type"""
    content: str
