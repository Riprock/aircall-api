"""Base resource class for all Aircall API resources."""

import logging


class BaseResource:
    """
    Base class for all API resource classes.

    Provides common functionality for making API requests and helper methods
    that all resource classes can use.
    """

    def __init__(self, client):
        """
        Initialize the resource with a client instance.

        Args:
            client: AircallClient instance
        """
        self._client = client
        self._logger = logging.getLogger(f'aircall.resources.{self.__class__.__name__}')

    def _get(self, endpoint: str, params: dict = None, **kwargs) -> dict:
        """
        Make a GET request.

        Args:
            endpoint: API endpoint
            params: Query parameters
            **kwargs: Additional arguments passed to _request()

        Returns:
            dict: Parsed JSON response
        """
        return self._client._request("GET", endpoint, params=params, **kwargs)

    def _post(self, endpoint: str, json: dict = None, **kwargs) -> dict:
        """
        Make a POST request.

        Args:
            endpoint: API endpoint
            json: Request body
            **kwargs: Additional arguments passed to _request()

        Returns:
            dict: Parsed JSON response
        """
        return self._client._request("POST", endpoint, json=json, **kwargs)

    def _put(self, endpoint: str, json: dict = None, **kwargs) -> dict:
        """
        Make a PUT request.

        Args:
            endpoint: API endpoint
            json: Request body
            **kwargs: Additional arguments passed to _request()

        Returns:
            dict: Parsed JSON response
        """
        return self._client._request("PUT", endpoint, json=json, **kwargs)

    def _delete(self, endpoint: str, **kwargs) -> dict:
        """
        Make a DELETE request.

        Args:
            endpoint: API endpoint
            **kwargs: Additional arguments passed to _request()

        Returns:
            dict: Parsed JSON response
        """
        return self._client._request("DELETE", endpoint, **kwargs)
