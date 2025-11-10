"""User models for Aircall API."""
from datetime import datetime
from typing import TYPE_CHECKING, Literal, Optional

from pydantic import BaseModel

if TYPE_CHECKING:
    from aircall.models.number import Number


class User(BaseModel):
    """
    User resource representing an Aircall user.

    Users can be Admins (Dashboard + Phone app access) or Agents (Phone app only).
    Users are assigned to Numbers.
    """
    id: int
    direct_link: str
    name: str  # Result of first_name + last_name
    email: str
    created_at: datetime

    # Availability fields
    available: bool  # Based on working hours
    availability_status: Literal["available", "custom", "unavailable"]
    substatus: str  # always_open, always_closed, or specific reason

    # Related resources
    numbers: list["Number"] = []

    # Settings
    time_zone: str  # Default: Etc/UTC
    language: str  # IETF language tag, default: en-US
    wrap_up_time: int  # Timer after call ends (seconds)


class UserAvailability(BaseModel):
    """
    Granular availability status for a user.

    Use the dedicated endpoint to retrieve these statuses.
    """
    available: Optional[bool] = None  # Ready to answer calls
    offline: Optional[bool] = None  # Not online
    do_not_disturb: Optional[bool] = None  # DND toggled
    in_call: Optional[bool] = None  # Currently on a call
    after_call_work: Optional[bool] = None  # Tagging/wrapping up
