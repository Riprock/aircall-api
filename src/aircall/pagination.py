"""Pagination support for Aircall list endpoints.

Aircall returns list responses as ``{"meta": {...}, "<resource>": [...]}``. The
SDK previously discarded ``meta`` entirely and handed back a bare list, so
callers had no way to learn the total, the current page, or whether another page
existed -- paging was impossible without hand-rolling the requests.

``Page`` carries both. It subclasses ``list`` so existing code that iterates,
indexes, takes ``len()`` or checks ``isinstance(result, list)`` keeps working
unchanged; only the extra metadata is new.
"""


from pydantic import BaseModel

#: Bounds Aircall enforces on the per_page query parameter.
MIN_PER_PAGE = 1
MAX_PER_PAGE = 50
DEFAULT_PER_PAGE = 20


class PageMeta(BaseModel):
    """The ``meta`` object returned alongside a paginated list.

    Every field is optional: not all Aircall list endpoints return a complete
    meta object, and some omit it entirely.
    """

    count: int | None = None
    total: int | None = None
    current_page: int | None = None
    per_page: int | None = None
    next_page_link: str | None = None
    previous_page_link: str | None = None


class Page(list):
    """A page of results plus the pagination metadata that came with it.

    Example:
        >>> page = client.call.list_calls(per_page=50)
        >>> for call in page:            # iterates like a list
        ...     print(call.id)
        >>> page.meta.total              # total across all pages
        2234
        >>> while page.has_next:
        ...     page = client.call.list_calls(page=page.meta.current_page + 1)
    """

    __slots__ = ("meta",)

    def __init__(self, items=(), meta: PageMeta | None = None):
        """
        Args:
            items: The parsed objects on this page
            meta: Parsed pagination metadata, or None if the endpoint sent none
        """
        super().__init__(items)
        self.meta = meta

    @property
    def has_next(self) -> bool:
        """Whether Aircall reported a further page after this one."""
        return bool(self.meta and self.meta.next_page_link)

    @property
    def has_previous(self) -> bool:
        """Whether Aircall reported a page before this one."""
        return bool(self.meta and self.meta.previous_page_link)

    @property
    def total(self) -> int | None:
        """Total matching items across all pages, if the endpoint reported it."""
        return self.meta.total if self.meta else None

    def __repr__(self) -> str:
        return f"Page({list(self)!r}, meta={self.meta!r})"


def validate_per_page(per_page: int, maximum: int = MAX_PER_PAGE) -> int:
    """
    Check a per_page value against the bounds Aircall enforces.

    Args:
        per_page: Requested page size
        maximum: Upper bound for this endpoint. Most cap at 50, but a few
            document a different limit (SMS templates allow 100).

    Returns:
        int: The value, unchanged, when it is in range

    Raises:
        ValueError: When outside the accepted range, which Aircall 400s on
    """
    if not MIN_PER_PAGE <= per_page <= maximum:
        raise ValueError(
            f"per_page must be between {MIN_PER_PAGE} and {maximum}, got {per_page}"
        )
    return per_page
