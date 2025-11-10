"""Number models for Aircall API."""
from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel

from aircall.models.user import User


class NumberMessages(BaseModel):
    """
    Music and Messages configuration for a Number.

    Custom audio files can be uploaded with public URLs.
    Check Aircall encoding recommendations first.
    """
    welcome: Optional[str] = None
    waiting: Optional[str] = None
    ringing_tone: Optional[str] = None
    unanswered_call: Optional[str] = None  # Deprecated
    after_hours: Optional[str] = None
    ivr: Optional[str] = None
    voicemail: Optional[str] = None
    closed: Optional[str] = None  # Deprecated
    callback_later: Optional[str] = None  # Deprecated


class Number(BaseModel):
    """
    Number resource representing an Aircall phone number.

    Numbers can be purchased and configured via Dashboard.
    Note: Several fields are deprecated due to Smartflows migration.
    """
    id: int
    direct_link: str
    name: str
    digits: str
    e164_digits: Optional[str] = None  # Only in webhook events
    created_at: datetime
    country: str
    time_zone: str

    # Deprecated: No longer updated for Smartflows
    open: Optional[bool] = None

    availability_status: Optional[Literal["open", "custom", "closed"]] = None

    # Deprecated: No longer supported
    is_ivr: Optional[bool] = None

    live_recording_activated: bool
    users: list["User"] = []
    priority: Optional[int] = None  # null, 0 (no priority), or 1 (top priority)
    messages: Optional[NumberMessages] = None
