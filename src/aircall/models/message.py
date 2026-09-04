"""Message models for Aircall API."""
from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel

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
    # Present on webhook payloads (message.received) but not on send responses
    external_number: Optional[str] = None
    body: str
    status: str
    raw_digits: str
    media_details: list[MediaDetail] = []
    # Send responses return plain URLs under media_url; inbound webhook payloads
    # return richer objects under media_details. They are different fields.
    media_url: list[str] = []
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


class GroupMessage(BaseModel):
    """
    A message sent to a group conversation.

    Group sends return a different shape to single sends: the recipients appear
    as a participants list, and the identifiers are group-scoped rather than a
    single message id.

    Read-only. Not updatable or destroyable via API.
    """

    group_message_id: str
    group_conversation_id: Optional[str] = None
    direct_link: Optional[str] = None
    direction: Optional[Literal["inbound", "outbound"]] = None
    status: Optional[str] = None
    participants: list[str] = []
    body: Optional[str] = None
    media_url: list[str] = []
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    sent_at: Optional[datetime] = None
    number: Optional["Number"] = None


class SmsTemplate(BaseModel):
    """An SMS template belonging to the company, aggregated across agents."""

    id: int
    name: Optional[str] = None
    body: Optional[str] = None


class WhatsAppLineStatus(BaseModel):
    """
    WhatsApp registration and health status of a WhatsApp-capable Number.

    Field names are camelCase because Aircall returns them that way on this
    endpoint, unlike the snake_case used elsewhere in the API.
    """

    wabaId: Optional[str] = None
    status: Optional[str] = None
    canSendMessage: Optional[bool] = None
    messagingLimitTier: Optional[str] = None
    qualityRating: Optional[str] = None
    businessVerificationStatus: Optional[str] = None
