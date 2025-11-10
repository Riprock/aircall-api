"""Resource module for managing messages"""
from aircall.resources.base import BaseResource
from aircall.models import Message


class MessageResource(BaseResource):
    """
    API Resource for Aircall Messages.

    Handles SMS, MMS, and WhatsApp messaging operations.
    All operations are scoped to a specific number.
    """

    def create_configuration(self, number_id: int, **kwargs) -> dict:
        """
        Create message configuration for a number.

        Args:
            number_id: The ID of the number
            **kwargs: Configuration data

        Returns:
            dict: Configuration response
        """
        return self._post(f"/numbers/{number_id}/messages/configuration", json=kwargs)

    def get_configuration(self, number_id: int) -> dict:
        """
        Fetch message configuration for a number.

        Args:
            number_id: The ID of the number

        Returns:
            dict: Configuration data
        """
        return self._get(f"/numbers/{number_id}/messages/configuration")

    def delete_configuration(self, number_id: int) -> dict:
        """
        Delete message configuration for a number.

        Args:
            number_id: The ID of the number

        Returns:
            dict: Delete configuration response
        """
        return self._delete(f"/numbers/{number_id}/messages/configuration")

    def send(self, number_id: int, to: str, body: str, **kwargs) -> Message:
        """
        Send a message from a number.

        Args:
            number_id: The ID of the number to send from
            to: Recipient phone number
            body: Message body
            **kwargs: Additional message data (media_details, etc.)

        Returns:
            Message: The sent message object
        """
        data = {"to": to, "body": body, **kwargs}
        response = self._post(f"/numbers/{number_id}/messages/send", json=data)
        return Message(**response["message"])

    def send_native(self, number_id: int, **kwargs) -> Message:
        """
        Send a native message (WhatsApp template) from a number.

        Args:
            number_id: The ID of the number to send from
            **kwargs: Native message data (template_id, parameters, etc.)

        Returns:
            Message: The sent message object
        """
        response = self._post(f"/numbers/{number_id}/messages/native/send", json=kwargs)
        return Message(**response["message"])
