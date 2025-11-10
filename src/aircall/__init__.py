"""Aircall API Python SDK."""

from aircall.client import AircallClient
from aircall.exceptions import (
    AircallAPIError,
    AircallConnectionError,
    AircallError,
    AircallPermissionError,
    AircallTimeoutError,
    AuthenticationError,
    NotFoundError,
    RateLimitError,
    ServerError,
    UnprocessableEntityError,
    ValidationError,
)
from aircall.logging_config import configure_logging

__all__ = [
    # Client
    "AircallClient",
    # Base exceptions
    "AircallError",
    "AircallAPIError",
    # API exceptions
    "AuthenticationError",
    "AircallPermissionError",
    "NotFoundError",
    "ValidationError",
    "UnprocessableEntityError",
    "RateLimitError",
    "ServerError",
    # Connection exceptions
    "AircallConnectionError",
    "AircallTimeoutError",
    # Logging
    "configure_logging",
]
