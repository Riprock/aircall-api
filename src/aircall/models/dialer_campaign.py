"""Dialer Campaign models for Aircall API."""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class DialerCampaignPhoneNumber(BaseModel):
    """Phone number in a dialer campaign"""
    id: int
    number: str
    called: bool
    created_at: datetime


class DialerCampaign(BaseModel):
    """Dialer Campaign (Power Dialer) resource"""
    id: int
    number_id: Optional[str] = None
    created_at: datetime
    phone_numbers: list[DialerCampaignPhoneNumber] = []
