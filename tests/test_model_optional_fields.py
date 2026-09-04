"""Fields Aircall omits from abridged payloads must not be required.

Aircall returns a full object at its own endpoint but an abridged one when the
same object is nested inside another. A model that marks those fields required
parses the standalone response and rejects the nested one.
"""

from aircall.models import Call, Message, User

from tests import payloads


def test_full_user_parses():
    user = User(**payloads.USER_FULL)
    assert user.substatus == "always_opened"
    assert user.wrap_up_time == 0


def test_user_nested_in_call_omits_substatus_and_wrap_up_time():
    user = User(**payloads.USER_NESTED_IN_CALL)
    assert user.substatus is None
    assert user.wrap_up_time is None
    assert user.time_zone == "America/New_York"


def test_posted_by_user_also_omits_time_zone_and_language():
    user = User(**payloads.USER_POSTED_BY)
    assert user.time_zone is None
    assert user.language is None


def test_documented_call_payload_parses_end_to_end():
    """The exact GET /v1/calls/:id example, nested abridged users included."""
    call = Call(**payloads.CALL)
    assert call.id == 812
    assert call.user.name == "John Doe"
    assert call.number.name == "French Office"
    assert call.comments[0].posted_by.id == 456


def test_message_send_response_omits_external_number():
    """Send responses carry no external_number; only webhook payloads do."""
    message = Message(**payloads.MESSAGE)
    assert message.external_number is None


def test_number_tolerates_undeclared_fields():
    """flow_editor_enabled appears in v2 responses but is not modelled yet."""
    from aircall.models import Number

    assert Number(**payloads.NUMBER_V2).id == 1234


def test_userv2_create_response_omits_substatus():
    """POST /v2/users returns no substatus, so it cannot be required."""
    from aircall.models import UserV2

    user = UserV2(**payloads.USER_V2_CREATED)
    assert user.substatus is None
    assert user.wrap_up_time == 0


def test_user_availability_is_a_string_not_booleans():
    """GET /v1/users/:id/availability returns {"availability": "..."}.

    The model previously declared five booleans, so it parsed that response into
    an object with every field None -- silently wrong rather than failing.
    """
    from aircall.models import UserAvailability

    single = UserAvailability(availability="after_call_work")
    assert single.availability == "after_call_work"
    assert single.id is None

    listed = UserAvailability(**payloads.USER_AVAILABILITY)
    assert (listed.id, listed.availability) == (456, "available")
