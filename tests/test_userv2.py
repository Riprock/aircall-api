"""User V2 resource behaviour.

User V1 is deprecated on 2026-09-30 and this is the migration target, so it has
to actually reach /v2 and return the V2 model.
"""

from aircall.models import Number, UserV2
from tests import payloads


def test_get_returns_the_v2_model(client, respond):
    respond({"user": payloads.USER_FULL})
    assert isinstance(client.userv2.get(456), UserV2)


def test_create_returns_the_v2_model(client, respond):
    respond({"user": payloads.USER_V2_CREATED})
    user = client.userv2.create(email="jeffrey.curtis@aircall.io", first_name="Jeffrey")
    assert isinstance(user, UserV2)
    assert client.session.last["json"]["email"] == "jeffrey.curtis@aircall.io"
    assert client.session.last["url"] == "https://api.aircall.io/v2/users"


def test_update_returns_the_v2_model(client, respond):
    respond({"user": payloads.USER_FULL})
    assert isinstance(client.userv2.update(456, first_name="A"), UserV2)


def test_list_returns_v2_models(client, respond):
    respond({"users": [payloads.USER_FULL], "meta": payloads.META})
    page = client.userv2.list_users()
    assert all(isinstance(u, UserV2) for u in page)


def test_get_numbers_returns_number_objects(client, respond):
    respond({"numbers": [payloads.NUMBER_V2], "meta": payloads.META})
    page = client.userv2.get_numbers(456)
    assert all(isinstance(n, Number) for n in page)
    assert page[0].name == "French Office"
    assert client.session.last["url"] == "https://api.aircall.io/v2/users/456/numbers"


def test_get_numbers_paginates(client, respond):
    respond({"numbers": [], "meta": payloads.META})
    client.userv2.get_numbers(456, page=2, per_page=5)
    assert client.session.last["params"] == {"page": 2, "per_page": 5}
