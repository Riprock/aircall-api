"""Resource module for managing contacts"""
from aircall.resources.base import BaseResource
from aircall.models import Contact


class ContactResource(BaseResource):
    """
    API Resource for Aircall Contacts.

    Handles operations relating to contacts including phone numbers and emails.
    """

    def list_contacts(self, page: int = 1, per_page: int = 20) -> list[Contact]:
        """
        List all contacts with pagination.

        Args:
            page: Page number (default 1)
            per_page: Results per page (default 20, max 50)

        Returns:
            list[Contact]: List of Contact objects
        """
        response = self._get("/contacts", params={"page": page, "per_page": per_page})
        return [Contact(**c) for c in response["contacts"]]

    def search(self, **params) -> list[Contact]:
        """
        Search for contacts with various filters.

        Args:
            **params: Search parameters (phone_number, email, etc.)

        Returns:
            list[Contact]: List of Contact objects matching the search criteria
        """
        response = self._get("/contacts/search", params=params)
        return [Contact(**c) for c in response["contacts"]]

    def get(self, contact_id: int) -> Contact:
        """
        Get a specific contact by ID.

        Args:
            contact_id: The ID of the contact to retrieve

        Returns:
            Contact: The contact object
        """
        response = self._get(f"/contacts/{contact_id}")
        return Contact(**response["contact"])

    def create(self, **kwargs) -> Contact:
        """
        Create a new contact.

        Args:
            **kwargs: Contact data (first_name, last_name, phone_numbers, emails, etc.)

        Returns:
            Contact: The created contact object
        """
        response = self._post("/contacts", json=kwargs)
        return Contact(**response["contact"])

    def update(self, contact_id: int, **kwargs) -> Contact:
        """
        Update a contact.

        Args:
            contact_id: The ID of the contact to update
            **kwargs: Contact fields to update

        Returns:
            Contact: The updated contact object
        """
        response = self._post(f"/contacts/{contact_id}", json=kwargs)
        return Contact(**response["contact"])

    def delete(self, contact_id: int) -> dict:
        """
        Delete a contact.

        Args:
            contact_id: The ID of the contact to delete

        Returns:
            dict: Delete response
        """
        return self._delete(f"/contacts/{contact_id}")

    def add_phone_number(self, contact_id: int, value: str, label: str = None) -> dict:
        """
        Add a phone number to a contact.

        Args:
            contact_id: The ID of the contact
            value: The phone number value
            label: Optional label for the phone number

        Returns:
            dict: Phone number response
        """
        data = {"value": value}
        if label:
            data["label"] = label
        return self._post(f"/contacts/{contact_id}/phone_details", json=data)

    def update_phone_number(self, contact_id: int, phone_number_id: int,
                          value: str = None, label: str = None) -> dict:
        """
        Update a phone number from a contact.

        Args:
            contact_id: The ID of the contact
            phone_number_id: The ID of the phone number to update
            value: New phone number value
            label: New label for the phone number

        Returns:
            dict: Update phone number response
        """
        data = {}
        if value:
            data["value"] = value
        if label:
            data["label"] = label
        return self._put(f"/contacts/{contact_id}/phone_details/{phone_number_id}", json=data)

    def delete_phone_number(self, contact_id: int, phone_number_id: int) -> dict:
        """
        Delete a phone number from a contact.

        Args:
            contact_id: The ID of the contact
            phone_number_id: The ID of the phone number to delete

        Returns:
            dict: Delete phone number response
        """
        return self._delete(f"/contacts/{contact_id}/phone_details/{phone_number_id}")

    def add_email(self, contact_id: int, value: str, label: str = None) -> dict:
        """
        Add an email to a contact.

        Args:
            contact_id: The ID of the contact
            value: The email address
            label: Optional label for the email

        Returns:
            dict: Email response
        """
        data = {"value": value}
        if label:
            data["label"] = label
        return self._post(f"/contacts/{contact_id}/email_details", json=data)

    def update_email(self, contact_id: int, email_id: int,
                    value: str = None, label: str = None) -> dict:
        """
        Update an email from a contact.

        Args:
            contact_id: The ID of the contact
            email_id: The ID of the email to update
            value: New email address
            label: New label for the email

        Returns:
            dict: Update email response
        """
        data = {}
        if value:
            data["value"] = value
        if label:
            data["label"] = label
        return self._put(f"/contacts/{contact_id}/email_details/{email_id}", json=data)

    def delete_email(self, contact_id: int, email_id: int) -> dict:
        """
        Delete an email from a contact.

        Args:
            contact_id: The ID of the contact
            email_id: The ID of the email to delete

        Returns:
            dict: Delete email response
        """
        return self._delete(f"/contacts/{contact_id}/email_details/{email_id}")
