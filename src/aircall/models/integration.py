"""Integration models for Aircall API."""
from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel

if TYPE_CHECKING:
    from aircall.models.user import User


class Integration(BaseModel):
    """Integration object representing connection state with third-party services"""
    name: str
    custom_name: Optional[str] = None
    logo: str
    company_id: int
    status: str
    active: bool
    number_ids: list[int] = []
    numbers_count: int
    user: Optional["User"] = None
