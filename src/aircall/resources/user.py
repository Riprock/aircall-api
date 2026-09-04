"""Resource module for managing users"""
from aircall.deprecation import USER_V1_SUNSET, warn_deprecated
from aircall.pagination import DEFAULT_PER_PAGE, Page
from aircall.resources.base import BaseResource
from aircall.models import User, UserAvailability


class UserResource(BaseResource):
    """
    API Resource for Aircall Users (V1).

    Handles operations relating to users including availability and outbound calls.

    .. deprecated:: 2.0.0
        Aircall deprecates the V1 list, retrieve, create and update endpoints on
        2026-09-30. Use ``client.userv2`` for those. The availability, outbound
        call and dial endpoints are not part of that deprecation and have no V2
        equivalent, so they remain here.
    """

    def list_users(self, page: int = 1, per_page: int = DEFAULT_PER_PAGE) -> Page:
        """
        List all users with pagination.

        Args:
            page: Page number (default 1)
            per_page: Results per page (1-50, default 20)

        .. deprecated:: 2.0.0
            Aircall removes this endpoint on 2026-09-30. Use ``client.userv2.list_users()``.

        Returns:
            Page: User objects, carrying .meta pagination details
        """
        warn_deprecated(
            "UserResource.list_users()", "client.userv2.list_users()", USER_V1_SUNSET
        )
        return self._list("/users", "users", User, page=page, per_page=per_page)

    def get(self, user_id: int) -> User:
        """
        Get a specific user by ID.

        Args:
            user_id: The ID of the user to retrieve

        .. deprecated:: 2.0.0
            Aircall removes this endpoint on 2026-09-30. Use ``client.userv2.get()``.

        Returns:
            User: The user object
        """
        warn_deprecated(
            "UserResource.get()", "client.userv2.get()", USER_V1_SUNSET
        )
        response = self._get(f"/users/{user_id}")
        return User(**response["user"])

    def create(self, email: str, **kwargs) -> User:
        """
        Create a new user.

        Args:
            email: User email address
            **kwargs: Additional user data (name, time_zone, language, etc.)

        .. deprecated:: 2.0.0
            Aircall removes this endpoint on 2026-09-30. Use ``client.userv2.create()``.

        Returns:
            User: The created user object
        """
        warn_deprecated(
            "UserResource.create()", "client.userv2.create()", USER_V1_SUNSET
        )
        data = {"email": email, **kwargs}
        response = self._post("/users", json=data)
        return User(**response["user"])

    def update(self, user_id: int, **kwargs) -> User:
        """
        Update a user.

        Args:
            user_id: The ID of the user to update
            **kwargs: User fields to update

        .. deprecated:: 2.0.0
            Aircall removes this endpoint on 2026-09-30. Use ``client.userv2.update()``.

        Returns:
            User: The updated user object
        """
        warn_deprecated(
            "UserResource.update()", "client.userv2.update()", USER_V1_SUNSET
        )
        response = self._put(f"/users/{user_id}", json=kwargs)
        return User(**response["user"])

    def delete(self, user_id: int) -> dict:
        """
        Delete a user.

        Args:
            user_id: The ID of the user to delete

        Returns:
            dict: Delete response
        """
        return self._delete(f"/users/{user_id}")

    def get_availabilities(
        self, page: int = 1, per_page: int = DEFAULT_PER_PAGE
    ) -> Page:
        """
        Retrieve availability status for all users.

        Args:
            page: Page number (default 1)
            per_page: Results per page (1-50, default 20)

        Returns:
            Page: UserAvailability objects, carrying .meta pagination details
        """
        return self._list(
            "/users/availabilities", "users", UserAvailability,
            page=page, per_page=per_page,
        )

    def get_availability(self, user_id: int) -> UserAvailability:
        """
        Check availability of a specific user.

        Args:
            user_id: The ID of the user

        Returns:
            UserAvailability: The user's current availability
        """
        response = self._get(f"/users/{user_id}/availability")
        return UserAvailability(**response)

    def start_call(self, user_id: int, to: str, **kwargs) -> dict:
        """
        Start an outbound call for a user.

        Args:
            user_id: The ID of the user making the call
            to: Phone number to call
            **kwargs: Additional call parameters

        Returns:
            dict: Call response
        """
        data = {"to": to, **kwargs}
        return self._post(f"/users/{user_id}/calls", json=data)

    def dial(self, user_id: int, **kwargs) -> dict:
        """
        Dial a number for a user.

        Args:
            user_id: The ID of the user
            **kwargs: Dial parameters

        Returns:
            dict: Dial response
        """
        return self._post(f"/users/{user_id}/dial", json=kwargs)
