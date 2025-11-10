"""Call models for Aircall API."""
from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel

from aircall.models.contact import Contact
from aircall.models.ivr_option import IVROption
from aircall.models.number import Number
from aircall.models.participant import Participant
from aircall.models.tag import Tag
from aircall.models.team import Team
from aircall.models.user import User


class CallComment(BaseModel):
    """
    Comment (Note) on a call.

    Can be created by Agents or via API.
    """
    id: int
    content: str
    posted_at: datetime
    posted_by: Optional["User"] = None  # Null if posted via API


class Call(BaseModel):
    """
    Call resource representing phone interactions.

    Three types:
    - Inbound: External person → Agent
    - Outbound: Agent → External person
    - Internal: Agent → Agent (not in Public API)

    Note: Call id is Int64 data type.
    """
    id: int  # Int64
    sid: Optional[str] = None  # Only in Call APIs (same as call_uuid)
    call_uuid: Optional[str] = None  # Only in Webhook events (same as sid)
    direct_link: str

    # Timestamps (Unix timestamps)
    started_at: datetime
    answered_at: Optional[datetime] = None  # Null if not answered
    ended_at: Optional[datetime] = None

    duration: int  # Seconds (ended_at - started_at, includes ringing)
    status: Literal["initial", "answered", "done"]
    direction: Literal["inbound", "outbound"]
    raw_digits: str  # International format or "anonymous"

    # Media URLs (valid for limited time)
    asset: Optional[str] = None  # Secured webpage for recording/voicemail
    recording: Optional[str] = None  # Direct MP3 URL (1 hour validity)
    recording_short_url: Optional[str] = None  # Short URL (3 hours validity)
    voicemail: Optional[str] = None  # Direct MP3 URL (1 hour validity)
    voicemail_short_url: Optional[str] = None  # Short URL (3 hours validity)

    archived: Optional[bool] = None
    missed_call_reason: Optional[Literal[
        "out_of_opening_hours",
        "short_abandoned",
        "abandoned_in_ivr",
        "abandoned_in_classic",
        "no_available_agent",
        "agents_did_not_answer"
    ]] = None

    cost: Optional[str] = None  # Deprecated - U.S. cents

    # Related objects
    number: Optional["Number"] = None
    user: Optional["User"] = None  # Who took or made the call
    contact: Optional["Contact"] = None
    assigned_to: Optional["User"] = None
    teams: list["Team"] = []  # Only for inbound calls

    # Transfer information
    transferred_by: Optional["User"] = None
    transferred_to: Optional["User"] = None  # First user of team if transferred to team
    external_transferred_to: Optional[str] = None  # Only via call.external_transferred event
    external_caller_number: Optional[str] = None  # Only via call.external_transferred event

    # Collections
    comments: list[CallComment] = []
    tags: list["Tag"] = []

    # Conference participants (referred as conference_participants in APIs)
    participants: list[Participant] = []

    # IVR options (requires fetch_call_timeline query param)
    ivr_options_selected: list["IVROption"] = []
