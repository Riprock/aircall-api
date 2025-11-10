"""Tag models for Aircall API."""
from typing import Optional

from pydantic import BaseModel


class Tag(BaseModel):
    """
    Tag resource for categorizing calls.

    Can be created by Admins in Dashboard or via API.
    Emojis cannot be used in Tag attributes (will be removed).
    """
    id: int
    direct_link: str
    name: str
    color: str  # Hexadecimal format (e.g., "#FF5733")
    description: Optional[str] = None
