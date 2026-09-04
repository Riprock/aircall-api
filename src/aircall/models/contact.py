"""Contact models for Aircall API."""

from pydantic import BaseModel


class PhoneNumber(BaseModel):
    """Phone number associated with a contact"""
    id: int
    label: str | None = None
    value: str


class Email(BaseModel):
    """Email address associated with a contact"""
    id: int
    label: str | None = None
    value: str


class Contact(BaseModel):
    """Contact resource from Aircall API"""
    id: int
    direct_link: str
    first_name: str | None = None
    last_name: str | None = None
    company_name: str | None = None
    description: str | None = None
    information: str | None = None
    is_shared: bool
    phone_numbers: list[PhoneNumber] = []
    emails: list[Email] = []
