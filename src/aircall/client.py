"""Aircall API client."""

import base64
import logging
import time
import requests
from requests.exceptions import Timeout, ConnectionError as RequestsConnectionError

from aircall.exceptions import (
    AircallAPIError,
    AircallConnectionError,
    AircallTimeoutError,
    AuthenticationError,
    #AircallPermissionError,
    NotFoundError,
    RateLimitError,
    ServerError,
    UnprocessableEntityError,
    ValidationError,
)
from aircall.resources import (
    CallResource,
    CompanyResource,
    ContactResource,
    DialerCampaignResource,
    IntegrationResource,
    MessageResource,
    NumberResource,
    TagResource,
    TeamResource,
    UserResource,
    WebhookResource,
)


class AircallClient:
    """
    Main client for interacting with the Aircall API.

    Handles authentication and provides access to all API resources.

    Example:
        >>> client = AircallClient(api_id="your_id", api_token="your_token")
        >>> numbers = client.number.list()
        >>> number = client.number.get(12345)
    """

    def __init__(
        self,
        api_id: str,
        api_token: str,
        timeout: int = 30,
        verbose: bool = False
    ) -> None:
        """
        Initialize the Aircall API client.

        Args:
            api_id: Your Aircall API ID
            api_token: Your Aircall API token
            timeout: Default request timeout in seconds (default: 30)
            verbose: Enable verbose logging for debugging (default: False)
                    When True, sets the logger level to DEBUG
        """
        self.base_url = "https://api.aircall.io/v1"
        credentials = base64.b64encode(f"{api_id}:{api_token}".encode()).decode('utf-8')
        self.timeout = timeout

        # Initialize logger
        self.logger = logging.getLogger('aircall.client')

        # If verbose is enabled, set logger to DEBUG level
        if verbose:
            self.logger.setLevel(logging.DEBUG)
            # Ensure handlers exist for the aircall logger
            aircall_logger = logging.getLogger('aircall')
            if not aircall_logger.handlers:
                handler = logging.StreamHandler()
                formatter = logging.Formatter(
                    fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S'
                )
                handler.setFormatter(formatter)
                aircall_logger.addHandler(handler)
                aircall_logger.setLevel(logging.DEBUG)

        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Basic {credentials}"})

        self.logger.info("Aircall client initialized")

        # Initialize resources
        self.call = CallResource(self)
        self.company = CompanyResource(self)
        self.contact = ContactResource(self)
        self.dialer_campaign = DialerCampaignResource(self)
        self.integration = IntegrationResource(self)
        self.message = MessageResource(self)
        self.number = NumberResource(self)
        self.tag = TagResource(self)
        self.team = TeamResource(self)
        self.user = UserResource(self)
        self.webhook = WebhookResource(self)

    def _request(
        self,
        method: str,
        endpoint: str,
        params: dict = None,
        json: dict = None,
        timeout: int = None
    ) -> dict:
        """
        Make an HTTP request to the Aircall API.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint (e.g., "/numbers", "/contacts/123")
            params: Query parameters as dict (e.g., {"page": 1, "per_page": 50})
            json: Request body as dict for POST/PUT requests
            timeout: Request timeout in seconds (uses self.timeout if not specified)

        Returns:
            dict: Parsed JSON response

        Raises:
            ValidationError: When request validation fails (400)
            AuthenticationError: When authentication fails (401 or 403)
            NotFoundError: When resource is not found (404)
            UnprocessableEntityError: When server cannot process request (422)
            RateLimitError: When rate limit is exceeded (429)
            ServerError: When server returns 5xx error
            AircallConnectionError: When connection to API fails
            AircallTimeoutError: When request times out
            AircallAPIError: For other API errors
        """
        url = self.base_url + endpoint

        # Log the request details
        self.logger.debug("Request: %s %s", method, url)
        if params:
            self.logger.debug("  Query params: %s", params)
        if json:
            self.logger.debug("  Request body: %s", json)

        start_time = time.time()

        try:
            # Use requests library to handle params and json automatically
            response = self.session.request(
                method=method,
                url=url,
                params=params,  # requests converts dict to query string
                json=json,      # requests converts dict to JSON body and sets Content-Type
                timeout=timeout or self.timeout
            )
        except Timeout as e:
            elapsed = time.time() - start_time
            self.logger.error(
                "Request timeout: %s %s - Failed after %ss (elapsed: %.2fs)",
                method, url, timeout or self.timeout, elapsed
            )
            raise AircallTimeoutError(
                f"Request to {url} timed out after {timeout or self.timeout} seconds"
            ) from e
        except RequestsConnectionError as e:
            elapsed = time.time() - start_time
            self.logger.error(
                "Connection error: %s %s - %s (elapsed: %.2fs)",
                method, url, str(e), elapsed
            )
            raise AircallConnectionError(
                f"Failed to connect to {url}: {str(e)}"
            ) from e

        elapsed = time.time() - start_time

        # Handle successful responses
        if 200 <= response.status_code < 300:
            self.logger.debug(
                "Response: %s %s %s (took %.2fs)",
                response.status_code, method, url, elapsed
            )
            if response.status_code == 204:  # No Content
                return {}
            return response.json()

        # Parse error response
        error_data = None
        error_message = response.reason
        try:
            error_data = response.json()
            if isinstance(error_data, dict):
                # Try to get message from various possible fields
                error_message = error_data.get('message') or error_data.get('error') or error_message
        except Exception:
            # If response is not JSON, use text content
            if response.text:
                error_message = response.text

        # Map status codes to appropriate exceptions based on Aircall API docs
        status_code = response.status_code

        # Log the error response
        self.logger.warning(
            "API error: %s %s %s - %s (took %.2fs)",
            status_code, method, url, error_message, elapsed
        )

        if status_code == 400:
            # Invalid payload/Bad Request
            raise ValidationError(
                error_message,
                status_code=status_code,
                response_data=error_data
            )
        if status_code == 401:
            raise AuthenticationError(
                error_message,
                status_code=status_code,
                response_data=error_data
            )
        if status_code == 403:
            # Forbidden - Invalid API key or Bearer access token
            raise AuthenticationError(
                error_message,
                status_code=status_code,
                response_data=error_data
            )
        if status_code == 404:
            # Not found - Id does not exist
            raise NotFoundError(
                error_message,
                status_code=status_code,
                response_data=error_data
            )
        if status_code == 422:
            # Server unable to process the request
            raise UnprocessableEntityError(
                error_message,
                status_code=status_code,
                response_data=error_data
            )
        if status_code == 429:
            # Rate limit exceeded
            retry_after = response.headers.get('Retry-After')
            if retry_after:
                self.logger.warning(
                    "Rate limit exceeded: %s %s - Retry after %ss",
                    method, url, retry_after
                )
            else:
                self.logger.warning("Rate limit exceeded (no retry-after header)")
            raise RateLimitError(
                error_message,
                status_code=status_code,
                response_data=error_data,
                retry_after=int(retry_after) if retry_after else None
            )
        if 500 <= status_code < 600:
            # Server errors
            raise ServerError(
                error_message,
                status_code=status_code,
                response_data=error_data
            )
        else:
            # Generic API error for other status codes
            raise AircallAPIError(
                error_message,
                status_code=status_code,
                response_data=error_data
            )
