"""IVR Option model for Aircall API."""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class IVROption(BaseModel):
    """
    IVR Option object representing IVR input from Smartflow-enabled number.

    Read-only. Available within call object when fetch_call_timeline=true.
    Only available for calls from last 2 months.
    All timestamps are in ISO 8601 format.
    """
    id: str
    title: str
    key: str
    branch: Optional[str] = None
    created_at: datetime
    transition_started_at: datetime
    transition_ended_at: datetime
