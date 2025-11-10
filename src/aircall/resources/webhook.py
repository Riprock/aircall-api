"""Resource module for managing webhooks"""
from aircall.resources.base import BaseResource
from aircall.models import Webhook


class WebhookResource(BaseResource):
    """
    API Resource for Aircall Webhooks.

    Webhooks are used to receive event notifications from Aircall.
    Use the token field to authenticate incoming webhook requests.
    """

    def list_webhooks(self, page: int = 1, per_page: int = 20) -> list[Webhook]:
        """
        List all webhooks with pagination.

        Args:
            page: Page number (default 1)
            per_page: Results per page (default 20, max 50)

        Returns:
            list[Webhook]: List of Webhook objects
        """
        response = self._get("/webhooks", params={"page": page, "per_page": per_page})
        return [Webhook(**w) for w in response["webhooks"]]

    def get(self, webhook_id: str) -> Webhook:
        """
        Get a specific webhook by ID.

        Args:
            webhook_id: The UUID of the webhook to retrieve

        Returns:
            Webhook: The webhook object
        """
        response = self._get(f"/webhooks/{webhook_id}")
        return Webhook(**response["webhook"])

    def create(self, url: str, events: list[str], custom_name: str = "Webhook", **kwargs) -> Webhook:
        """
        Create a new webhook.

        Args:
            url: Valid URL to your web server
            events: List of event names to subscribe to
            custom_name: Custom name for the webhook (default: "Webhook")
            **kwargs: Additional webhook data

        Returns:
            Webhook: The created webhook object
        """
        data = {"url": url, "events": events, "custom_name": custom_name, **kwargs}
        response = self._post("/webhooks", json=data)
        return Webhook(**response["webhook"])

    def update(self, webhook_id: str, **kwargs) -> Webhook:
        """
        Update a webhook.

        Args:
            webhook_id: The UUID of the webhook to update
            **kwargs: Webhook fields to update (url, events, custom_name, active, etc.)

        Returns:
            Webhook: The updated webhook object
        """
        response = self._put(f"/webhooks/{webhook_id}", json=kwargs)
        return Webhook(**response["webhook"])

    def delete(self, webhook_id: str) -> dict:
        """
        Delete a webhook.

        Args:
            webhook_id: The UUID of the webhook to delete

        Returns:
            dict: Delete response
        """
        return self._delete(f"/webhooks/{webhook_id}")
