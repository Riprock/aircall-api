"""Every resource method parses Aircall's documented response.

This is the regression guard for the 1.2.0 breakage, where ten of sixteen read
paths raised on the first call. Each case runs the real request path against a
recorded payload, so a model that cannot parse what Aircall documents fails
here rather than in a user's integration.
"""

import pytest

from aircall.models import (
    Call,
    Company,
    Contact,
    DialerCampaign,
    Integration,
    Message,
    Number,
    Tag,
    Team,
    User,
    UserV2,
    Webhook,
)
from tests import payloads

# (id, response payload, call, expected result type)
CASES = [
    ("user.get", {"user": payloads.USER_FULL},
     lambda c: c.user.get(456), User),
    ("user.list_users", {"users": [payloads.USER_FULL]},
     lambda c: c.user.list_users(), list),
    ("userv2.get", {"user": payloads.USER_FULL},
     lambda c: c.userv2.get(456), UserV2),
    ("userv2.get_numbers", {"numbers": [payloads.NUMBER_V2]},
     lambda c: c.userv2.get_numbers(456), list),
    ("user.get_availabilities", {"users": [payloads.USER_AVAILABILITY]},
     lambda c: c.user.get_availabilities(), list),
    ("dialer_campaign.get_phone_numbers",
     {"numbers": payloads.DIALER_CAMPAIGN["phone_numbers"]},
     lambda c: c.dialer_campaign.get_phone_numbers(456), list),
    ("userv2.list_users", {"users": [payloads.USER_FULL]},
     lambda c: c.userv2.list_users(), list),
    ("call.get", {"call": payloads.CALL},
     lambda c: c.call.get(812), Call),
    ("call.list_calls", {"calls": [payloads.CALL]},
     lambda c: c.call.list_calls(), list),
    ("call.search", {"calls": [payloads.CALL]},
     lambda c: c.call.search(), list),
    ("number.get", {"number": payloads.NUMBER},
     lambda c: c.number.get(1234), Number),
    ("number.list_numbers", {"numbers": [payloads.NUMBER]},
     lambda c: c.number.list_numbers(), list),
    ("contact.get", {"contact": payloads.CONTACT},
     lambda c: c.contact.get(710), Contact),
    ("contact.list_contacts", {"contacts": [payloads.CONTACT]},
     lambda c: c.contact.list_contacts(), list),
    ("team.get", {"team": payloads.TEAM},
     lambda c: c.team.get(678), Team),
    ("team.list_teams", {"teams": [payloads.TEAM]},
     lambda c: c.team.list_teams(), list),
    ("tag.get", {"tag": payloads.TAG},
     lambda c: c.tag.get(1), Tag),
    ("tag.list_tags", {"tags": [payloads.TAG]},
     lambda c: c.tag.list_tags(), list),
    ("company.get", {"company": payloads.COMPANY},
     lambda c: c.company.get(), Company),
    ("webhook.get", {"webhook": payloads.WEBHOOK},
     lambda c: c.webhook.get("wh-1"), Webhook),
    ("webhook.list_webhooks", {"webhooks": [payloads.WEBHOOK]},
     lambda c: c.webhook.list_webhooks(), list),
    ("integration.get", {"integration": payloads.INTEGRATION},
     lambda c: c.integration.get(), Integration),
    ("dialer_campaign.get", {"dialer_campaign": payloads.DIALER_CAMPAIGN},
     lambda c: c.dialer_campaign.get(456), DialerCampaign),
]


@pytest.mark.parametrize(
    "payload,call,expected", [c[1:] for c in CASES], ids=[c[0] for c in CASES]
)
def test_resource_parses_documented_response(client, respond, payload, call, expected):
    respond(payload)
    result = call(client)
    assert isinstance(result, expected)
    if isinstance(result, list):
        assert result, "list responses should not silently parse to empty"


def test_list_of_calls_parses_nested_objects(client, respond):
    """Nested user, number and comment objects survive list parsing."""
    respond({"calls": [payloads.CALL]})
    call = client.call.list_calls()[0]
    assert call.user.name == "John Doe"
    assert call.number.id == 1234
    assert call.comments[0].content == "Please call back this customer!"


def test_no_content_response_returns_empty_dict(client, respond):
    """204 responses have no body and must not be handed to .json()."""
    respond(None, status_code=204)
    assert client.tag.delete(1) == {}


def test_message_send_parses_documented_response(client, respond):
    """Aircall returns the message object unwrapped, with no "message" key."""
    respond(payloads.MESSAGE)
    message = client.message.send_skipping_inbox(123, "+130", "hi")
    assert isinstance(message, Message)
    assert message.id == "messageId"


def test_userv2_get_numbers_returns_numbers(client, respond):
    """/v2 returns full Number objects under "numbers", not a "number_ids" list."""
    respond({"numbers": [payloads.NUMBER_V2], "meta": {"total": 1}})
    numbers = client.userv2.get_numbers(456)
    assert [n.id for n in numbers] == [1234]
    assert numbers.meta.total == 1
