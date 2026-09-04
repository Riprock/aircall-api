"""List endpoints expose Aircall's pagination metadata.

Every list_* method previously returned a bare list and discarded the meta
object, so callers could not learn the total or whether another page existed.
Page keeps both while still behaving as a list, so iteration, indexing, len()
and isinstance(x, list) all keep working.
"""

import pytest

from aircall import Page, PageMeta
from aircall.pagination import MAX_PER_PAGE, validate_per_page

from tests import payloads


def test_page_still_behaves_like_a_list(client, respond):
    respond({"calls": [payloads.CALL], "meta": payloads.META})
    page = client.call.list_calls()
    assert isinstance(page, list)
    assert len(page) == 1
    assert page[0].id == 812
    assert [c.id for c in page] == [812]


def test_meta_is_parsed(client, respond):
    respond({"calls": [payloads.CALL], "meta": payloads.META})
    page = client.call.list_calls()
    assert isinstance(page.meta, PageMeta)
    assert page.meta.total == 2234
    assert page.meta.current_page == 1
    assert page.total == 2234


def test_has_next_and_previous(client, respond):
    respond({"calls": [payloads.CALL], "meta": payloads.META})
    page = client.call.list_calls()
    assert page.has_next is True
    assert page.has_previous is False


def test_missing_meta_is_tolerated(client, respond):
    """Not every list endpoint returns a meta object."""
    respond({"calls": [payloads.CALL]})
    page = client.call.list_calls()
    assert page.meta is None
    assert page.has_next is False
    assert page.total is None


def test_missing_result_key_yields_empty_page(client, respond):
    respond({"meta": payloads.META})
    assert client.call.list_calls() == []


def test_page_and_per_page_reach_the_query_string(client, respond):
    respond({"calls": [], "meta": payloads.META})
    client.call.list_calls(page=3, per_page=50)
    assert client.session.last["params"]["page"] == 3
    assert client.session.last["params"]["per_page"] == 50


def test_search_filters_are_merged_with_pagination(client, respond):
    respond({"calls": [], "meta": payloads.META})
    client.call.search(per_page=25, **{"from": 1584998199, "order": "desc"})
    params = client.session.last["params"]
    assert params["from"] == 1584998199
    assert params["order"] == "desc"
    assert params["per_page"] == 25


@pytest.mark.parametrize("bad", [0, -1, 51, 100])
def test_per_page_outside_aircall_bounds_is_rejected(client, bad):
    """Aircall 400s on per_page outside 1-50; fail before spending the request."""
    with pytest.raises(ValueError, match="per_page must be between"):
        client.call.list_calls(per_page=bad)
    assert client.session.calls == [], "no request should have been made"


@pytest.mark.parametrize("good", [1, 20, MAX_PER_PAGE])
def test_per_page_within_bounds_is_accepted(good):
    assert validate_per_page(good) == good


def test_every_list_method_returns_a_page(client, respond):
    """A list method that forgets the helper would silently lose meta."""
    cases = [
        ({"users": [payloads.USER_FULL]}, lambda c: c.user.list_users()),
        ({"users": [payloads.USER_FULL]}, lambda c: c.userv2.list_users()),
        ({"calls": [payloads.CALL]}, lambda c: c.call.list_calls()),
        ({"calls": [payloads.CALL]}, lambda c: c.call.search()),
        ({"contacts": [payloads.CONTACT]}, lambda c: c.contact.list_contacts()),
        ({"contacts": [payloads.CONTACT]}, lambda c: c.contact.search()),
        ({"numbers": [payloads.NUMBER]}, lambda c: c.number.list_numbers()),
        ({"tags": [payloads.TAG]}, lambda c: c.tag.list_tags()),
        ({"teams": [payloads.TEAM]}, lambda c: c.team.list_teams()),
        ({"webhooks": [payloads.WEBHOOK]}, lambda c: c.webhook.list_webhooks()),
        ({"numbers": [payloads.NUMBER_V2]}, lambda c: c.userv2.get_numbers(1)),
        ({"users": [payloads.USER_AVAILABILITY]},
         lambda c: c.user.get_availabilities()),
    ]
    for payload, call in cases:
        respond({**payload, "meta": payloads.META})
        page = call(client)
        assert isinstance(page, Page), call
        assert page.meta.total == 2234
