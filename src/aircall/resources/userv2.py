"""Resource module for managing users via the v2 API"""
from aircall.pagination import DEFAULT_PER_PAGE, Page
from aircall.resources.base import BaseResource
from aircall.models import Number, UserV2


class UserV2Resource(BaseResource):
    """
    API Resource for Aircall Users V2.

    User V2 is the replacement for User V1, which Aircall deprecates on
    2026-09-30. Every request is routed to /v2; see BaseResource._api_version.

    Note the V2 User object carries no ``numbers`` field. Use get_numbers() to
    retrieve the Numbers assigned to a User.
    """

    _api_version = "v2"

    def list_users(self, page: int = 1, per_page: int = DEFAULT_PER_PAGE) -> Page:
        """
        List all users with pagination.

        Args:
            page: Page number (default 1)
            per_page: Results per page (1-50, default 20)

        Returns:
            Page: UserV2 objects, carrying .meta pagination details
        """
        return self._list("/users", "users", UserV2, page=page, per_page=per_page)

    def get(self, user_id: int) -> UserV2:
        """
        Get a specific user by ID.

        Args:
            user_id: The ID of the user to retrieve, or their email address

        Returns:
            UserV2: The user object
        """
        response = self._get(f"/users/{user_id}")
        return UserV2(**response["user"])

    def create(self, email: str, **kwargs) -> UserV2:
        """
        Create a new user.

        Args:
            email: User email address
            **kwargs: Additional user data (first_name, last_name, time_zone,
                language, wrap_up_time, role_ids, inviter_user_id)

        Returns:
            UserV2: The created user object
        """
        data = {"email": email, **kwargs}
        response = self._post("/users", json=data)
        return UserV2(**response["user"])

    def update(self, user_id: int, **kwargs) -> UserV2:
        """
        Update a user.

        Args:
            user_id: The ID of the user to update
            **kwargs: User fields to update

        Returns:
            UserV2: The updated user object
        """
        response = self._put(f"/users/{user_id}", json=kwargs)
        return UserV2(**response["user"])

    def get_numbers(
        self, user_id: int, page: int = 1, per_page: int = DEFAULT_PER_PAGE
    ) -> Page:
        """
        Get the Numbers assigned to a user.

        Aircall returns full Number objects under the "numbers" key, paginated.
        This previously read a "number_ids" key that the API never sends.

        Args:
            user_id: The ID of the user
            page: Page number (default 1)
            per_page: Results per page (1-50, default 20)

        Returns:
            Page: Number objects assigned to the user
        """
        return self._list(
            f"/users/{user_id}/numbers", "numbers", Number,
            page=page, per_page=per_page,
        )
