"""Contact models for Aircall API."""
from typing import Optional

from pydantic import BaseModel


class PhoneNumber(BaseModel):
    """Phone number associated with a contact"""
    id: int
    label: Optional[str] = None
    value: str


class Email(BaseModel):
    """Email address associated with a contact"""
    id: int
    label: Optional[str] = None
    value: str


class Contact(BaseModel):
    """Contact resource from Aircall API"""
    id: int
    direct_link: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    company_name: Optional[str] = None
    description: Optional[str] = None
    information: Optional[str] = None
    is_shared: bool
    phone_numbers: list[PhoneNumber] = []
    emails: list[Email] = []
