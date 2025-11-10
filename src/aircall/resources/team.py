"""Resource module for managing teams"""
from aircall.resources.base import BaseResource
from aircall.models import Team


class TeamResource(BaseResource):
    """
    API Resource for Aircall Teams.

    Teams are used to group users for call distribution.
    Team names must be unique within a company (max 64 characters).
    """

    def list_teams(self, page: int = 1, per_page: int = 20) -> list[Team]:
        """
        List all teams with pagination.

        Args:
            page: Page number (default 1)
            per_page: Results per page (default 20, max 50)

        Returns:
            list[Team]: List of Team objects
        """
        response = self._get("/teams", params={"page": page, "per_page": per_page})
        return [Team(**t) for t in response["teams"]]

    def get(self, team_id: int) -> Team:
        """
        Get a specific team by ID.

        Args:
            team_id: The ID of the team to retrieve

        Returns:
            Team: The team object
        """
        response = self._get(f"/teams/{team_id}")
        return Team(**response["team"])

    def create(self, name: str, **kwargs) -> Team:
        """
        Create a new team.

        Args:
            name: Team name (max 64 characters, must be unique in company)
            **kwargs: Additional team data

        Returns:
            Team: The created team object
        """
        data = {"name": name, **kwargs}
        response = self._post("/teams", json=data)
        return Team(**response["team"])

    def delete(self, team_id: int) -> dict:
        """
        Delete a team.

        Args:
            team_id: The ID of the team to delete

        Returns:
            dict: Delete response
        """
        return self._delete(f"/teams/{team_id}")

    def add_user(self, team_id: int, user_id: int) -> dict:
        """
        Add a user to a team.

        Args:
            team_id: The ID of the team
            user_id: The ID of the user to add

        Returns:
            dict: Add user response
        """
        return self._post(f"/teams/{team_id}/users/{user_id}")

    def remove_user(self, team_id: int, user_id: int) -> dict:
        """
        Remove a user from a team.

        Args:
            team_id: The ID of the team
            user_id: The ID of the user to remove

        Returns:
            dict: Remove user response
        """
        return self._delete(f"/teams/{team_id}/users/{user_id}")
