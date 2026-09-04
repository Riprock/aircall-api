"""Base resource class for all Aircall API resources."""

import logging
from typing import Optional


class BaseResource:
    """
    Base class for all API resource classes.

    Provides common functionality for making API requests and helper methods
    that all resource classes can use.

    Subclasses that target a non-default Aircall API version declare it once via
    the ``_api_version`` class attribute rather than passing ``version=`` at each
    call site, so a single resource cannot end up split across two versions.
    """

    #: Aircall API version this resource targets. Override in subclasses.
    _api_version = "v1"

    def __init__(self, client):
        """
        Initialize the resource with a client instance.

        Args:
            client: AircallClient instance
        """
        self._client = client
        self._logger = logging.getLogger(f'aircall.resources.{self.__class__.__name__}')

    def _get(self, endpoint: str, params: dict = None, version: Optional[str] = None, **kwargs) -> dict:
        """
        Make a GET request.

        Args:
            endpoint: API endpoint
            params: Query parameters
            version: API version override; defaults to the resource's _api_version
            **kwargs: Additional arguments passed to _request()

        Returns:
            dict: Parsed JSON response
        """
        return self._client._request(
            "GET", endpoint, params=params, version=version or self._api_version, **kwargs
        )

    def _post(self, endpoint: str, json: dict = None, version: Optional[str] = None, **kwargs) -> dict:
        """
        Make a POST request.

        Args:
            endpoint: API endpoint
            json: Request body
            version: API version override; defaults to the resource's _api_version
            **kwargs: Additional arguments passed to _request()

        Returns:
            dict: Parsed JSON response
        """
        return self._client._request(
            "POST", endpoint, json=json, version=version or self._api_version, **kwargs
        )

    def _put(self, endpoint: str, json: dict = None, version: Optional[str] = None, **kwargs) -> dict:
        """
        Make a PUT request.

        Args:
            endpoint: API endpoint
            json: Request body
            version: API version override; defaults to the resource's _api_version
            **kwargs: Additional arguments passed to _request()

        Returns:
            dict: Parsed JSON response
        """
        return self._client._request(
            "PUT", endpoint, json=json, version=version or self._api_version, **kwargs
        )

    def _delete(self, endpoint: str, version: Optional[str] = None, **kwargs) -> dict:
        """
        Make a DELETE request.

        Args:
            endpoint: API endpoint
            version: API version override; defaults to the resource's _api_version
            **kwargs: Additional arguments passed to _request()

        Returns:
            dict: Parsed JSON response
        """
        return self._client._request(
            "DELETE", endpoint, version=version or self._api_version, **kwargs
        )
