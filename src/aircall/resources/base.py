"""Base resource class for all Aircall API resources."""

import logging
from typing import Optional

from aircall.pagination import (
    DEFAULT_PER_PAGE,
    MAX_PER_PAGE,
    Page,
    PageMeta,
    validate_per_page,
)


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

    def _list(
        self,
        endpoint: str,
        key: str,
        model=None,
        *,
        page: int = 1,
        per_page: int = DEFAULT_PER_PAGE,
        params: Optional[dict] = None,
        version: Optional[str] = None,
        max_per_page: int = MAX_PER_PAGE,
    ) -> Page:
        """
        Fetch one page of a list endpoint, preserving its pagination metadata.

        Args:
            endpoint: API endpoint
            key: Response key holding the array (e.g. "calls", "users")
            model: Pydantic model to parse each item with; None leaves raw dicts
            page: Page number
            per_page: Results per page (1-50)
            params: Extra query parameters, merged with page/per_page
            version: API version override; defaults to the resource's _api_version
            max_per_page: Upper bound on per_page for this endpoint

        Returns:
            Page: The parsed items, carrying .meta

        Raises:
            ValueError: When per_page falls outside the range Aircall accepts
        """
        query = dict(params or {})
        query["page"] = page
        query["per_page"] = validate_per_page(per_page, max_per_page)
        response = self._get(endpoint, params=query, version=version)
        return self._as_page(response, key, model)

    @staticmethod
    def _as_page(response: dict, key: str, model=None) -> Page:
        """
        Wrap a raw list response in a Page.

        Args:
            response: Parsed JSON body
            key: Response key holding the array
            model: Pydantic model to parse each item with; None leaves raw dicts

        Returns:
            Page: The parsed items, carrying .meta when the response included one
        """
        items = response.get(key) or []
        parsed = [model(**item) for item in items] if model else list(items)
        meta = response.get("meta")
        return Page(parsed, PageMeta(**meta) if meta else None)

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
