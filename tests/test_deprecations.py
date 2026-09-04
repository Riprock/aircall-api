"""Deprecated endpoints warn, and name their replacement and removal date.

Aircall retires the User V1 list/retrieve/create/update endpoints on 2026-09-30,
and the realtime_transcription endpoint's date (2026-03-31) has already passed.
Callers should learn that from a warning rather than from a 404 one morning.
"""

import warnings

import pytest

from tests import payloads

# Aircall's announcement covers exactly these four V1 endpoints.
DEPRECATED_USER_CALLS = [
    ("list_users", {"users": [payloads.USER_FULL]}, lambda c: c.user.list_users()),
    ("get", {"user": payloads.USER_FULL}, lambda c: c.user.get(456)),
    ("create", {"user": payloads.USER_FULL}, lambda c: c.user.create("a@b.io")),
    ("update", {"user": payloads.USER_FULL}, lambda c: c.user.update(456, first_name="A")),
]

# Not part of the announcement, and with no V2 equivalent: these must stay quiet.
UNAFFECTED_USER_CALLS = [
    ("delete", {}, lambda c: c.user.delete(456)),
    ("get_availability", {"availability": "available"},
     lambda c: c.user.get_availability(456)),
    ("get_availabilities", {"users": [payloads.USER_AVAILABILITY]},
     lambda c: c.user.get_availabilities()),
    ("start_call", {}, lambda c: c.user.start_call(456, to="+130")),
    ("dial", {}, lambda c: c.user.dial(456, to="+130")),
]


@pytest.mark.parametrize(
    "payload,call", [c[1:] for c in DEPRECATED_USER_CALLS],
    ids=[c[0] for c in DEPRECATED_USER_CALLS],
)
def test_deprecated_user_v1_calls_warn(client, respond, payload, call):
    respond(payload)
    with pytest.warns(DeprecationWarning) as record:
        call(client)
    message = str(record[0].message)
    assert "client.userv2" in message, "the warning must name the replacement"
    assert "2026-09-30" in message, "the warning must name the removal date"


@pytest.mark.parametrize(
    "payload,call", [c[1:] for c in UNAFFECTED_USER_CALLS],
    ids=[c[0] for c in UNAFFECTED_USER_CALLS],
)
def test_user_endpoints_outside_the_announcement_do_not_warn(
    client, respond, payload, call
):
    respond(payload)
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        call(client)
    assert [w for w in caught if issubclass(w.category, DeprecationWarning)] == []


def test_userv2_never_warns(client, respond):
    """The migration target must not warn, or the advice is circular."""
    respond({"user": payloads.USER_FULL})
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        client.userv2.get(456)
        client.userv2.update(456, first_name="A")
    assert [w for w in caught if issubclass(w.category, DeprecationWarning)] == []


def test_warning_points_at_the_callers_line(client, respond):
    """stacklevel must blame the caller, not the SDK's own module."""
    respond({"user": payloads.USER_FULL})
    with pytest.warns(DeprecationWarning) as record:
        client.user.get(456)
    assert record[0].filename == __file__


def test_realtime_transcription_warns_that_the_date_has_passed(client, respond):
    respond({"transcription": {}})
    with pytest.warns(DeprecationWarning) as record:
        client.call.get_realtime_transcription(812)
    message = str(record[0].message)
    assert "has passed" in message
    assert '2026-03-31' in message
    assert 'mode="realtime"' in message


def test_realtime_transcription_still_calls_the_old_endpoint(client, respond):
    """Warning only. Silently retargeting would change behaviour unannounced."""
    respond({"transcription": {}})
    with pytest.warns(DeprecationWarning):
        client.call.get_realtime_transcription(812)
    assert client.session.last["url"].endswith("/calls/812/realtime_transcription")


def test_transcription_mode_is_sent_as_a_query_param(client, respond):
    respond({"transcription": {}})
    client.call.get_transcription(812, mode="realtime")
    assert client.session.last["params"] == {"mode": "realtime"}


def test_transcription_without_mode_sends_no_param(client, respond):
    respond({"transcription": {}})
    client.call.get_transcription(812)
    assert client.session.last["params"] is None


def test_transcription_rejects_an_unknown_mode(client):
    with pytest.raises(ValueError, match="mode must be one of"):
        client.call.get_transcription(812, mode="streaming")
    assert client.session.calls == [], "no request should have been made"


def test_transcription_does_not_warn(client, respond):
    respond({"transcription": {}})
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        client.call.get_transcription(812, mode="realtime")
    assert [w for w in caught if issubclass(w.category, DeprecationWarning)] == []
