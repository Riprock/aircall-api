"""User V2 models for Aircall API."""
from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel


# Availability status values for granular user status
AvailabilityStatusType = Literal[
    "available",       # Agent ready to answer calls
    "offline",         # Agent not online
    "do_not_disturb",  # Agent toggled themselves as do not disturb
    "in_call",         # Agent is currently on a call
    "after_call_work", # Agent is performing after-call work (tagging/wrapping up)
]

# Working status values
WorkingStatusType = Literal["available", "custom", "unavailable"]

# Substatus values when user is unavailable
SubstatusType = Literal[
    "always_open",    # When available or custom
    "always_closed",  # When unavailable with no specific reason
    "Out for lunch",
    "On a break",
    "In training",
    "Back office",
    "Other",
]


class UserV2(BaseModel):
    """
    User V2 resource representing an Aircall user.

    Users can be either Admins or Agents:
    - Admins: can access the Dashboard and the Phone app, and can invite other users.
    - Agents: can only access the Phone app and recording files.

    Note: User V2 object does NOT include the numbers object.
    """
    id: int
    """Unique identifier for the User."""

    direct_link: str
    """Direct API URL."""

    name: str
    """Full name of the User. Results of first_name + last_name."""

    email: str
    """Email of the User."""

    created_at: datetime
    """Timestamp when the User was created, in UTC."""

    available: bool
    """Current availability status of the User, based on their working hours."""

    availability_status: WorkingStatusType
    """
    Current working status of the User.
    Can be 'available', 'custom' (available according to Working Hours and Timezone),
    or 'unavailable' (Do Not Disturb or other unavailable status).
    """

    substatus: str
    """
    Current substatus of the User.
    - If availability_status is 'available' or 'custom': substatus will be 'always_open'.
    - If availability_status is 'unavailable' without a selected reason: 'always_closed'.
    - If availability_status is 'unavailable' with a selected reason: the specific reason
      (e.g., 'Out for lunch', 'On a break', 'In training', 'Back office', 'Other').
    """

    time_zone: str = "Etc/UTC"
    """
    The User's timezone. Can be set from the Dashboard or Phone app.
    Default is Etc/UTC.
    """

    language: str = "en-US"
    """
    The User's preferred language. Can be set from the Dashboard or Phone app.
    Format is IETF language tag. Default is en-US.
    """

    wrap_up_time: int
    """
    A pre-set timer triggered after a call has ended, during which the user
    can't receive any calls. Value is in seconds.
    """


class UserV2Availability(BaseModel):
    """
    Granular availability status for a User V2.

    These statuses provide more detail about why a user may or may not be available.
    """
    available: Optional[str] = None
    """Agent ready to answer calls."""

    offline: Optional[str] = None
    """Agent not online."""

    do_not_disturb: Optional[str] = None
    """Agent toggled themselves as do not disturb."""

    in_call: Optional[str] = None
    """Agent is currently on a call."""

    after_call_work: Optional[str] = None
    """Agent is performing their after-call work (tagging a call or wrapping up)."""
