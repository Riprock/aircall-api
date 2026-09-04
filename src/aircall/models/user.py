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
    # Omitted from user objects nested inside Call payloads
    substatus: Optional[str] = None  # always_open, always_closed, or specific reason

    # Related resources
    numbers: list["Number"] = []

    # Settings
    # All three are omitted from abridged user objects nested in other payloads
    # (Call.user, Call.comments[].posted_by), so they cannot be required.
    time_zone: Optional[str] = None  # Default: Etc/UTC
    language: Optional[str] = None  # IETF language tag, default: en-US
    wrap_up_time: Optional[int] = None  # Timer after call ends (seconds)


class UserAvailability(BaseModel):
    """
    Granular availability status for a User.

    Aircall reports this as a single string, not a set of booleans:
    GET /v1/users/:id/availability returns {"availability": "after_call_work"},
    and GET /v1/users/availabilities returns the same object per user with an id.

    Documented values are available, offline, do_not_disturb, in_call and
    after_call_work. Left as a plain str rather than a Literal so a value Aircall
    adds later does not break parsing.
    """
    id: Optional[int] = None  # Absent on the single-user endpoint
    availability: str
