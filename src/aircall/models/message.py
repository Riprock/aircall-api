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
    external_number: str | None = None
    body: str
    status: str
    raw_digits: str
    media_details: list[MediaDetail] = []
    # Send responses return plain URLs under media_url; inbound webhook payloads
    # return richer objects under media_details. They are different fields.
    media_url: list[str] = []
    created_at: datetime
    updated_at: datetime
    sent_at: datetime | None = None

    # Channel-specific fields
    channel: Literal["whatsapp"] | None = None  # null for SMS/MMS

    # WhatsApp-specific fields
    template_content: str | None = None
    type: str | None = None
    metadata: str | None = None
    parent_id: str | None = None
    whatsapp_message_category: Literal["marketing", "utility", "authentication"] | None = None
    whatsapp_message_type: Literal["regular", "free_entry_point", "free_customer_serivce"] | None = None
    recipient_country: str | None = None

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
    group_conversation_id: str | None = None
    direct_link: str | None = None
    direction: Literal["inbound", "outbound"] | None = None
    status: str | None = None
    participants: list[str] = []
    body: str | None = None
    media_url: list[str] = []
    created_at: datetime | None = None
    updated_at: datetime | None = None
    sent_at: datetime | None = None
    number: Optional["Number"] = None


class SmsTemplate(BaseModel):
    """An SMS template belonging to the company, aggregated across agents."""

    id: int
    name: str | None = None
    body: str | None = None


class WhatsAppLineStatus(BaseModel):
    """
    WhatsApp registration and health status of a WhatsApp-capable Number.

    Field names are camelCase because Aircall returns them that way on this
    endpoint, unlike the snake_case used elsewhere in the API.
    """

    wabaId: str | None = None
    status: str | None = None
    canSendMessage: bool | None = None
    messagingLimitTier: str | None = None
    qualityRating: str | None = None
    businessVerificationStatus: str | None = None
