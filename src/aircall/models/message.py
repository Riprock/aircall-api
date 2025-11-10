"""Message models for Aircall API."""
from datetime import datetime
from typing import TYPE_CHECKING, Literal, Optional

from pydantic import BaseModel

if TYPE_CHECKING:
    from aircall.models.contact import Contact
    from aircall.models.number import Number


class MediaDetail(BaseModel):
    """Media file attached to a message"""
    file_name: str
    file_type: str
    presigned_url: str


class Message(BaseModel):
    """
    Message object for SMS, MMS, and WhatsApp communications.

    Read-only. Not updatable or destroyable via API.
    WhatsApp-specific attributes won't be present for SMS/MMS.
    """
    id: str
    direct_link: str
    direction: Literal["inbound", "outbound"]
    external_number: str
    body: str
    status: str
    raw_digits: str
    media_details: list[MediaDetail] = []
    created_at: datetime
    updated_at: datetime
    sent_at: Optional[datetime] = None

    # Channel-specific fields
    channel: Optional[Literal["whatsapp"]] = None  # null for SMS/MMS

    # WhatsApp-specific fields
    template_content: Optional[str] = None
    type: Optional[str] = None
    metadata: Optional[str] = None
    parent_id: Optional[str] = None
    whatsapp_message_category: Optional[Literal["marketing", "utility", "authentication"]] = None
    whatsapp_message_type: Optional[Literal["regular", "free_entry_point", "free_customer_serivce"]] = None
    recipient_country: Optional[str] = None

    # Related objects
    number: Optional["Number"] = None
    contact: Optional["Contact"] = None
