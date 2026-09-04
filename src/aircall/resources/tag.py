"""Resource module for managing tags"""
from aircall.models import Tag
from aircall.pagination import DEFAULT_PER_PAGE, Page
from aircall.resources.base import BaseResource


class TagResource(BaseResource):
    """
    API Resource for Aircall Tags.

    Tags are used to categorize calls and can be created by Admins.
    Note: Emojis cannot be used in tag attributes and will be removed.
    """

    def list_tags(self, page: int = 1, per_page: int = DEFAULT_PER_PAGE) -> Page:
        """
        List all tags with pagination.

        Args:
            page: Page number (default 1)
            per_page: Results per page (1-50, default 20)

        Returns:
            Page: Tag objects, carrying .meta pagination details
        """
        return self._list("/tags", "tags", Tag, page=page, per_page=per_page)

    def get(self, tag_id: int) -> Tag:
        """
        Get a specific tag by ID.

        Args:
            tag_id: The ID of the tag to retrieve

        Returns:
            Tag: The tag object
        """
        response = self._get(f"/tags/{tag_id}")
        return Tag(**response["tag"])

    def create(self, name: str, color: str, description: str | None = None) -> Tag:
        """
        Create a new tag.

        Args:
            name: Tag name (emojis will be removed)
            color: Tag color in hexadecimal format (e.g., "#FF5733")
            description: Optional tag description

        Returns:
            Tag: The created tag object
        """
        data = {"name": name, "color": color}
        if description:
            data["description"] = description
        response = self._post("/tags", json=data)
        return Tag(**response["tag"])

    def update(self, tag_id: int, **kwargs) -> Tag:
        """
        Update a tag.

        Args:
            tag_id: The ID of the tag to update
            **kwargs: Tag fields to update (name, color, description)

        Returns:
            Tag: The updated tag object
        """
        response = self._put(f"/tags/{tag_id}", json=kwargs)
        return Tag(**response["tag"])

    def delete(self, tag_id: int) -> dict:
        """
        Delete a tag.

        Args:
            tag_id: The ID of the tag to delete

        Returns:
            dict: Delete response
        """
        return self._delete(f"/tags/{tag_id}")
