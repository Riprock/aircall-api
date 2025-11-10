"""Team models for Aircall API."""
from datetime import datetime

from pydantic import BaseModel

from aircall.models.user import User


class Team(BaseModel):
    """
    Team resource for grouping users.

    Teams are used in call distributions of Numbers.
    Name must be unique in a company (max 64 characters).
    """
    id: int
    direct_link: str
    name: str  # Max 64 characters, must be unique in company
    created_at: datetime
    users: list[User] = []
