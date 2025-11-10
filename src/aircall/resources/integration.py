"""Resource module for managing integrations"""
from aircall.resources.base import BaseResource
from aircall.models import Integration


class IntegrationResource(BaseResource):
    """
    API Resource for Aircall Integrations.

    Handles operations for managing third-party integrations.
    """

    def get(self) -> Integration:
        """
        Retrieve integration information for the current API client.

        Returns:
            Integration: The integration object

        Example:
            >>> integration = client.integration.get()
            >>> print(integration.name, integration.active)
        """
        response = self._get("/integrations/me")
        return Integration(**response["integration"])

    def enable(self) -> Integration:
        """
        Enable the integration.

        Returns:
            Integration: The updated integration object

        Example:
            >>> integration = client.integration.enable()
            >>> print(integration.active)  # True
        """
        response = self._post("/integrations/enable")
        return Integration(**response["integration"])

    def disable(self) -> Integration:
        """
        Disable the integration.

        Returns:
            Integration: The updated integration object

        Example:
            >>> integration = client.integration.disable()
            >>> print(integration.active)  # False
        """
        response = self._post("/integrations/disable")
        return Integration(**response["integration"])
