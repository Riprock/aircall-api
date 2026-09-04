"""Response payloads copied from Aircall's published API reference.

These are transcribed from the examples at https://developers.aircall.io/api-references
so the models are tested against what Aircall actually documents returning, not
against what the models happen to expect.

Note the three User shapes. Aircall abridges nested user objects, and the
abridgement differs by position -- this is what made a fully-required User model
fail on real call payloads.
"""

# GET /v1/users -- the complete User object
USER_FULL = {
    "id": 456,
    "direct_link": "https://api.aircall.io/v1/users/456",
    "name": "John Doe",
    "email": "john.doe@aircall.io",
    "available": True,
    "availability_status": "available",
    "substatus": "always_opened",
    "created_at": "2019-12-29T10:03:18.000Z",
    "time_zone": "America/New_York",
    "language": "en-US",
    "wrap_up_time": 0,
}

# Call.user -- no substatus, no wrap_up_time
USER_NESTED_IN_CALL = {
    "id": 456,
    "direct_link": "https://api.aircall.io/v1/users/456",
    "name": "John Doe",
    "email": "john.doe@aircall.io",
    "available": True,
    "availability_status": "available",
    "created_at": "2019-12-29T10:03:18.000Z",
    "time_zone": "America/New_York",
    "language": "en-US",
}

# Call.comments[].posted_by -- also drops time_zone and language
USER_POSTED_BY = {
    "id": 456,
    "direct_link": "https://api.aircall.io/v1/users/456",
    "name": "Johnn Doe",
    "email": "john.doe@aircall.io",
    "available": True,
    "availability_status": "available",
    "created_at": "2019-12-29T10:03:18.000Z",
}

NUMBER = {
    "id": 1234,
    "direct_link": "https://api.aircall.io/v1/numbers/1234",
    "name": "French Office",
    "digits": "+33 1 76 11 11 11",
    "created_at": "2020-01-02T11:41:01.000Z",
    "country": "FR",
    "time_zone": "Europe/Paris",
    "open": True,
    "availability_status": "custom",
    "is_ivr": True,
    "live_recording_activated": True,
    "priority": None,
    "messages": {
        "welcome": "https://example.com/welcome.mp3",
        "waiting": "https://example.com/waiting_music.mp3",
        "ivr": "https://example.com/ivr_message.mp3",
        "voicemail": "https://example.com/voicemail.mp3",
        "closed": "https://example.com/closed_message.mp3",
        "callback_later": "https://example.com/callback_later.mp3",
        "unanswered_call": "https://example.com/unanswered_call.mp3",
        "after_hours": "https://example.com/after_hours.mp3",
        "ringing_tone": "https://example.com/ringing_tone.mp3",
    },
}

# GET /v2/users/:id/numbers returns Numbers carrying flow_editor_enabled,
# which the Number model does not yet declare. Pydantic ignores unknown keys
# by default, so this asserts the extra field does not break parsing.
NUMBER_V2 = {**NUMBER, "flow_editor_enabled": True}

CALL = {
    "id": 812,
    "sid": "CA1234567890",
    "direct_link": "https://api.aircall.io/v1/calls/812",
    "direction": "outbound",
    "status": "done",
    "missed_call_reason": None,
    "started_at": 1584998199,
    "answered_at": 1584998205,
    "ended_at": 1584998210,
    "duration": 11,
    "voicemail": None,
    "recording": None,
    "asset": None,
    "raw_digits": "+1 800-123-4567",
    "user": USER_NESTED_IN_CALL,
    "contact": None,
    "archived": False,
    "assigned_to": None,
    "transferred_by": None,
    "transferred_to": None,
    "cost": "2.34",
    "number": NUMBER,
    "comments": [
        {
            "id": 735,
            "content": "Please call back this customer!",
            "posted_at": 1587994808,
            "posted_by": USER_POSTED_BY,
        }
    ],
    "tags": [],
}

CONTACT = {
    "id": 710,
    "direct_link": "https://api.aircall.io/v1/contacts/710",
    "first_name": "Nathan",
    "last_name": "Melka",
    "company_name": "Aircall",
    "information": "Best contact ever",
    "is_shared": False,
    "phone_numbers": [
        {"id": 123, "label": "Work", "value": "+33 1 76 11 11 11"}
    ],
    "emails": [
        {"id": 456, "label": "Work", "value": "nathan@aircall.io"}
    ],
}

TEAM = {
    "id": 678,
    "direct_link": "https://api.aircall.io/v1/teams/678",
    "name": "Sales",
    "created_at": "2020-01-02T11:41:01.000Z",
    "users": [USER_FULL],
}

TAG = {
    "id": 1,
    "direct_link": "https://api.aircall.io/v1/tags/1",
    "name": "Interested",
    "color": "#0033CC",
    "description": None,
}

COMPANY = {"name": "Aircall", "users_count": 12, "numbers_count": 3}

WEBHOOK = {
    "webhook_id": "0d3e5b1a-3b1a-4c1a-9c1a-0d3e5b1a3b1a",
    "direct_link": "https://api.aircall.io/v1/webhooks/26316",
    "created_at": "2020-01-02T11:41:01.000Z",
    "custom_name": "My Webhook",
    "url": "https://example.com/hook",
    "active": True,
    "token": "abc123",
    "events": ["call.created", "call.ended"],
}

INTEGRATION = {
    "name": "Zapier",
    "custom_name": None,
    "logo": "https://example.com/logo.png",
    "company_id": 1,
    "status": "installed",
    "active": True,
    "number_ids": [1234],
    "numbers_count": 1,
    "user": USER_FULL,
}

# POST /v1/numbers/:id/messages/send -- note Aircall returns the object at the
# top level, with no "message" envelope, and without external_number.
MESSAGE = {
    "id": "messageId",
    "status": "pending",
    "direct_link": "https://api.aircall.io/v1/numbers/123/messages/SM123",
    "direction": "outbound",
    "created_at": "2024-07-30T07:29:21.000Z",
    "sent_at": "2024-07-30T07:29:21.000Z",
    "updated_at": "2024-07-30T07:29:21.000Z",
    "raw_digits": "+130...",
    "body": "text you want to send",
}

DIALER_CAMPAIGN = {
    "id": 1,
    "number_id": "1234",
    "created_at": "2020-01-02T11:41:01.000Z",
    "phone_numbers": [
        {
            "id": 1,
            "number": "+33 1 76 11 11 11",
            "called": False,
            "created_at": "2020-01-02T11:41:01.000Z",
        }
    ],
}
