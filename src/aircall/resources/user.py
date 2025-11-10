"""Resource module for managing users"""
from aircall.resources.base import BaseResource
from aircall.models import User, UserAvailability


class UserResource(BaseResource):
    """
    API Resource for Aircall Users.

    Handles operations relating to users including availability and outbound calls.
    """

    def list_users(self, page: int = 1, per_page: int = 20) -> list[User]:
        """
        List all users with pagination.

        Args:
            page: Page number (default 1)
            per_page: Results per page (default 20, max 50)

        Returns:
            list[User]: List of User objects
        """
        response = self._get("/users", params={"page": page, "per_page": per_page})
        return [User(**u) for u in response["users"]]

    def get(self, user_id: int) -> User:
        """
        Get a specific user by ID.

        Args:
            user_id: The ID of the user to retrieve

        Returns:
            User: The user object
        """
        response = self._get(f"/users/{user_id}")
        return User(**response["user"])

    def create(self, email: str, **kwargs) -> User:
        """
        Create a new user.

        Args:
            email: User email address
            **kwargs: Additional user data (name, time_zone, language, etc.)

        Returns:
            User: The created user object
        """
        data = {"email": email, **kwargs}
        response = self._post("/users", json=data)
        return User(**response["user"])

    def update(self, user_id: int, **kwargs) -> User:
        """
        Update a user.

        Args:
            user_id: The ID of the user to update
            **kwargs: User fields to update

        Returns:
            User: The updated user object
        """
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

    def get_availabilities(self) -> dict:
        """
        Retrieve availability status for all users.

        Returns:
            dict: Dictionary of user availabilities
        """
        return self._get("/users/availabilities")

    def get_availability(self, user_id: int) -> UserAvailability:
        """
        Check availability of a specific user.

        Args:
            user_id: The ID of the user

        Returns:
            UserAvailability: Granular availability status
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
