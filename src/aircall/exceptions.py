"""Custom exceptions for the Aircall API client."""


class AircallError(Exception):
    """Base exception for all Aircall errors"""


class AircallAPIError(AircallError):
    """Raised when the API returns an error response"""

    def __init__(self, message, status_code=None, response_data=None):
        self.message = message
        self.status_code = status_code
        self.response_data = response_data
        super().__init__(self.message)


class AuthenticationError(AircallAPIError):
    """Raised when authentication fails (401)"""


class AircallPermissionError(AircallAPIError):
    """Raised when user lacks permission (403)"""


class NotFoundError(AircallAPIError):
    """Raised when resource not found (404)"""


class ValidationError(AircallAPIError):
    """Raised when request validation fails (400)"""


class UnprocessableEntityError(AircallAPIError):
    """Raised when server unable to process the request (422)"""


class RateLimitError(AircallAPIError):
    """Raised when rate limit exceeded (429)"""

    def __init__(self, message, retry_after=None, **kwargs):
        super().__init__(message, **kwargs)
        self.retry_after = retry_after  # Seconds until can retry


class ServerError(AircallAPIError):
    """Raised when server returns 5xx error"""


class AircallConnectionError(AircallError):
    """Raised when connection to API fails"""


class AircallTimeoutError(AircallError):
    """Raised when request times out"""
