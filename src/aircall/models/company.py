"""Company model for Aircall API."""
from pydantic import BaseModel


class Company(BaseModel):
    """
    Company object representing an Aircall company.

    Read-only. Not updatable or destroyable via API.
    Can only be modified via Aircall Dashboard.
    """
    name: str
    users_count: int
    numbers_count: int
