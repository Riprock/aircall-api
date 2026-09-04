"""Resource module for managing dialer campaigns"""
from aircall.pagination import Page
from aircall.resources.base import BaseResource
from aircall.models import DialerCampaign, DialerCampaignPhoneNumber


class DialerCampaignResource(BaseResource):
    """
    API Resource for Aircall Dialer Campaigns (Power Dialer).

    All operations are scoped to a specific user.
    """

    def get(self, user_id: int) -> DialerCampaign:
        """
        Retrieve a user's dialer campaign.

        Args:
            user_id: The ID of the user

        Returns:
            DialerCampaign: The dialer campaign object
        """
        response = self._get(f"/users/{user_id}/dialer_campaign")
        return DialerCampaign(**response["dialer_campaign"])

    def create(self, user_id: int, **kwargs) -> DialerCampaign:
        """
        Create a dialer campaign for a user.

        Args:
            user_id: The ID of the user
            **kwargs: Dialer campaign data (number_id, phone_numbers, etc.)

        Returns:
            DialerCampaign: The created dialer campaign object
        """
        response = self._post(f"/users/{user_id}/dialer_campaign", json=kwargs)
        return DialerCampaign(**response["dialer_campaign"])

    def delete(self, user_id: int) -> dict:
        """
        Delete a user's dialer campaign.

        Args:
            user_id: The ID of the user

        Returns:
            dict: Delete response
        """
        return self._delete(f"/users/{user_id}/dialer_campaign")

    def get_phone_numbers(self, user_id: int) -> Page:
        """
        Retrieve phone numbers from a user's dialer campaign.

        Aircall returns these under the "numbers" key; reading "phone_numbers"
        silently yielded an empty list on every call.

        Args:
            user_id: The ID of the user

        Returns:
            Page: DialerCampaignPhoneNumber objects in the campaign
        """
        response = self._get(f"/users/{user_id}/dialer_campaign/phone_numbers")
        return self._as_page(response, "numbers", DialerCampaignPhoneNumber)

    def add_phone_numbers(self, user_id: int, phone_numbers: list[str]) -> dict:
        """
        Add phone numbers to a user's dialer campaign.

        Args:
            user_id: The ID of the user
            phone_numbers: List of phone numbers to add

        Returns:
            dict: Add phone numbers response
        """
        return self._post(f"/users/{user_id}/dialer_campaign/phone_numbers",
                         json={"phone_numbers": phone_numbers})

    def delete_phone_number(self, user_id: int, phone_number_id: int) -> dict:
        """
        Delete a phone number from a user's dialer campaign.

        Args:
            user_id: The ID of the user
            phone_number_id: The ID of the phone number to delete

        Returns:
            dict: Delete phone number response
        """
        return self._delete(f"/users/{user_id}/dialer_campaign/phone_numbers/{phone_number_id}")
