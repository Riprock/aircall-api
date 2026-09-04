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

# POST /v2/users -- note the absence of substatus
USER_V2_CREATED = {
    "id": 458,
    "direct_link": "https://api.aircall.io/v2/users/458",
    "name": "Jeffrey Curtis",
    "email": "jeffrey.curtis@aircall.io",
    "available": False,
    "availability_status": "available",
    "created_at": "2020-02-18T20:52:22.000Z",
    "time_zone": "Etc/UTC",
    "language": "en-US",
    "wrap_up_time": 0,
}

# GET /v1/users/availabilities -- availability is a string, not booleans
USER_AVAILABILITY = {"id": 456, "availability": "available"}

# The meta object Aircall attaches to every paginated list response
META = {
    "count": 20,
    "total": 2234,
    "current_page": 1,
    "per_page": 20,
    "next_page_link": "https://api.aircall.io/v1/calls?page=2&per_page=20",
    "previous_page_link": None,
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


# --- Phase 4: new endpoint responses -------------------------------------

# POST /v1/numbers/:id/messages/group/send
GROUP_MESSAGE = {
    "group_message_id": "8f3c2c4e-9c6c-4c8e-9b4a-2c1f7e3d9c52",
    "status": "pending",
    "direct_link": "https://api.aircall.io/v1/numbers/123/messages/SM1",
    "direction": "outbound",
    "created_at": 1722317361216,
    "sent_at": 1722317361216,
    "updated_at": 1722317361216,
    "group_conversation_id": "c4b8c1c0-0c6e-4c3f-9c1c-5c2f8e7a91d4",
    "participants": ["+13000000001", "+13000000002"],
    "media_url": [],
    "body": "text you want to send",
}

# GET /v1/sms/templates
SMS_TEMPLATE = {"id": 8821, "name": "order_update", "body": "Your order is on its way."}

# GET /v1/numbers/:id/templates -- cursor pagination, no "meta" envelope
WHATSAPP_TEMPLATES = {
    "templates": [
        {
            "id": 1,
            "wabaId": "123456789",
            "name": "order_confirmation",
            "category": "UTILITY",
            "status": "APPROVED",
            "language": "en",
        }
    ],
    "pageInfo": {"currentToken": 0, "nextToken": 10, "totalCount": 50},
}

# GET /v1/numbers/:id/whatsapp_status
WHATSAPP_STATUS = {
    "wabaId": "123456789",
    "status": "ONLINE",
    "canSendMessage": True,
    "messagingLimitTier": "TIER_1K",
    "qualityRating": "GREEN",
    "businessVerificationStatus": "VERIFIED",
}

# POST /v1/outbound-calls/agents/:agent_id -- 202 Accepted
OUTBOUND_CALL = {
    "id": "01ARZ3NDEKTSV4RRFFQ69G5FAV",
    "idempotency_key": "appt-reminder-2024-03-15-cust-12345",
    "status": "PENDING",
    "virtual_agent_id": "agent-abc123",
}

# POST /v1/analytics/report/export
ANALYTICS_EXPORT_PENDING = {
    "exportID": "9d3f2a1e-2b6c-4f0a-9c3e-1a2b3c4d5e6f",
    "createdAt": "2026-05-20T09:35:12.000Z",
    "status": "PENDING",
}

ANALYTICS_EXPORT_COMPLETE = {
    "exportID": "9d3f2a1e-2b6c-4f0a-9c3e-1a2b3c4d5e6f",
    "createdAt": "2026-05-20T09:35:12.000Z",
    "status": "COMPLETED",
    "format": "CSV",
    "exportName": "calls-history-may-2026",
    "isZipCompressed": False,
    "downloadUrl": "https://aircall-analytics-exports.s3.amazonaws.com/x.csv",
    "downloadUrlExpiresAt": "2026-05-20T10:35:12.000Z",
}

ANALYTICS_EXPORT_FAILED = {
    "exportID": "9d3f2a1e-2b6c-4f0a-9c3e-1a2b3c4d5e6f",
    "createdAt": "2026-05-20T09:35:12.000Z",
    "status": "FAILED",
    "errorMessage": "Report generation failed: too many rows",
}

# GET /v1/calls/:call_id/predicted_csat
PREDICTED_CSAT = {
    "csat": {
        "call_id": 5237603,
        "call_uuid": "CAFFEE343770a4b19d6289ebee7f406a7b",
        "score": 75,
        "drivers": [
            {"polarity": "POSITIVE", "label": "Customer was satisfied"},
        ],
    }
}
