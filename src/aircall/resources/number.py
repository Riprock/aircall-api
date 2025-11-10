"""Number resource for managing Aircall phone numbers."""

from aircall.resources.base import BaseResource
from aircall.models import Number


class NumberResource(BaseResource):
    """
    API resource for Aircall phone numbers.

    Handles operations related to phone numbers including listing,
    retrieving, updating, and checking registration status.
    """

    def list_numbers(self, page: int = 1, per_page: int = 20) -> list[Number]:
        """
        List all numbers with pagination.

        Args:
            page: Page number (default 1)
            per_page: Results per page (default 20, max 50)

        Returns:
            list[Number]: List of Number objects

        Note:
            Response includes pagination metadata in 'meta' field:
            - count: Items in current page
            - total: Total items
            - current_page: Current page number
            - next_page_link: URL to next page (if available)
            - previous_page_link: URL to previous page (if available)

        Example:
            >>> numbers = client.number.list_numbers(page=1, per_page=50)
            >>> for number in numbers:
            ...     print(number.name, number.digits)
        """
        response = self._get("/numbers", params={"page": page, "per_page": per_page})
        return [Number(**n) for n in response["numbers"]]

    def get(self, number_id: int) -> Number:
        """
        Retrieve a specific number by ID.

        Args:
            number_id: Unique identifier for the number

        Returns:
            Number: Number object

        Raises:
            Exception: If number not found (404) or other API error

        Example:
            >>> number = client.number.get(12345)
            >>> print(number.name, number.digits)
        """
        response = self._get(f"/numbers/{number_id}")
        return Number(**response["number"])

    def update(self, number_id: int, **kwargs) -> Number:
        """
        Update a number's configuration.

        Args:
            number_id: Unique identifier for the number
            **kwargs: Fields to update (e.g., name, priority)

        Returns:
            Number: Updated Number object

        Example:
            >>> number = client.number.update(12345, name="Sales Line", priority=1)
            >>> print(number.name)  # "Sales Line"
        """
        response = self._put(f"/numbers/{number_id}", json=kwargs)
        return Number(**response["number"])

    def get_registration_status(self, number_id: int) -> dict:
        """
        Get registration status for a number.

        Args:
            number_id: Unique identifier for the number

        Returns:
            dict: Registration status information

        Example:
            >>> status = client.number.get_registration_status(12345)
            >>> print(status)
        """
        return self._get(f"/numbers/{number_id}/registration_status")
