"""Webhook Model File"""
from datetime import datetime

from pydantic import BaseModel, Field



class Webhook(BaseModel):
    """
    Webhook resource for receiving event notifications.

    Composed of a custom_name and list of events.
    Use the token field to identify which Aircall account sent the webhook.
    """
    webhook_id: str = Field(..., description="UUID identifier for the webhook")
    direct_link: str
    created_at: datetime
    custom_name: str = "Webhook"  # Default value
    url: str  # Valid URL to web server
    active: bool = True  # Default is true
    token: str  # Unique token for authentication
    events: list[str] = []  # List of registered event names
