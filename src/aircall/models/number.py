"""Number models for Aircall API."""
from datetime import datetime
from typing import Literal

from pydantic import BaseModel

from aircall.models.user import User


class NumberMessages(BaseModel):
    """
    Music and Messages configuration for a Number.

    Custom audio files can be uploaded with public URLs.
    Check Aircall encoding recommendations first.
    """
    welcome: str | None = None
    waiting: str | None = None
    ringing_tone: str | None = None
    unanswered_call: str | None = None  # Deprecated
    after_hours: str | None = None
    ivr: str | None = None
    voicemail: str | None = None
    closed: str | None = None  # Deprecated
    callback_later: str | None = None  # Deprecated


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
    e164_digits: str | None = None  # Only in webhook events
    created_at: datetime
    country: str
    time_zone: str

    # Deprecated: No longer updated for Smartflows
    open: bool | None = None

    availability_status: Literal["open", "custom", "closed"] | None = None

    # Deprecated: No longer supported
    is_ivr: bool | None = None

    live_recording_activated: bool
    users: list["User"] = []
    priority: int | None = None  # null, 0 (no priority), or 1 (top priority)
    messages: NumberMessages | None = None
    # Whether the Number is managed by the Smartflows editor
    flow_editor_enabled: bool | None = None
