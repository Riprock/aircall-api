"""Resource module for managing company information"""
from aircall.resources.base import BaseResource
from aircall.models import Company


class CompanyResource(BaseResource):
    """
    API Resource for Aircall Company.

    Provides read-only access to company information.
    Companies cannot be updated or deleted via the API.
    """

    def get(self) -> Company:
        """
        Get company information.

        Returns:
            Company: Company object with name, users_count, and numbers_count

        Note:
            Companies are read-only and can only be modified via the Aircall Dashboard.

        Example:
            >>> company = client.company.get()
            >>> print(company.name, company.users_count, company.numbers_count)
        """
        response = self._get("/company")
        return Company(**response["company"])
