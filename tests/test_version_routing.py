"""Requests reach the API version their resource declares.

client.py defined base_url_v2 but _request hardcoded base_url, so every
UserV2Resource call silently went to /v1 -- making userv2.get() a duplicate of
user.get() and userv2.get_numbers() a 404.
"""

import pytest

from tests import payloads


def test_v1_resource_targets_v1(client, respond):
    respond({"user": payloads.USER_FULL})
    client.user.get(456)
    assert client.session.last["url"] == "https://api.aircall.io/v1/users/456"


def test_v2_resource_targets_v2(client, respond):
    respond({"user": payloads.USER_FULL})
    client.userv2.get(456)
    assert client.session.last["url"] == "https://api.aircall.io/v2/users/456"


def test_v2_resource_targets_v2_on_every_verb(client, respond):
    """A resource must not end up split across versions, verb by verb."""
    respond({"users": [payloads.USER_FULL]})
    client.userv2.list_users()
    assert client.session.last["url"].startswith("https://api.aircall.io/v2/")

    respond({"user": payloads.USER_FULL})
    client.userv2.create(email="a@b.io")
    assert client.session.last["url"].startswith("https://api.aircall.io/v2/")

    client.userv2.update(456, first_name="A")
    assert client.session.last["url"].startswith("https://api.aircall.io/v2/")

    client.userv2.get(456)
    assert client.session.last["url"].startswith("https://api.aircall.io/v2/")


@pytest.mark.parametrize(
    "resource,payload,call",
    [
        ("call", {"call": payloads.CALL}, lambda c: c.call.get(812)),
        ("contact", {"contact": payloads.CONTACT}, lambda c: c.contact.get(710)),
        ("number", {"number": payloads.NUMBER}, lambda c: c.number.get(1234)),
        ("team", {"team": payloads.TEAM}, lambda c: c.team.get(678)),
        ("company", {"company": payloads.COMPANY}, lambda c: c.company.get()),
    ],
)
def test_v1_resources_stay_on_v1(client, respond, resource, payload, call):
    respond(payload)
    call(client)
    assert client.session.last["url"].startswith("https://api.aircall.io/v1/")


def test_unknown_version_is_rejected(client):
    with pytest.raises(ValueError, match="Unknown Aircall API version"):
        client._request("GET", "/users", version="v3")


def test_explicit_version_overrides_the_resource_default(client, respond):
    """The per-call escape hatch still works for one-off endpoints."""
    respond({"user": payloads.USER_FULL})
    client.user._get("/users/456", version="v2")
    assert client.session.last["url"] == "https://api.aircall.io/v2/users/456"
