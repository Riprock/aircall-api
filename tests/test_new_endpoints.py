"""Endpoints Aircall added since the last sync (2026-01-20).

Each test pins the exact path and body, because several of these break the
conventions used elsewhere in the API: the WhatsApp sends are not scoped under
/numbers/:id and name their recipient field differently from each other, and the
Analytics endpoints use camelCase.
"""

import pytest

from aircall.models import (
    AnalyticsExport, GroupMessage, Message, OutboundCallRequest,
    SmsTemplate, WhatsAppLineStatus,
)

from tests import payloads

BASE = "https://api.aircall.io/v1"


# --- Conversation Intelligence ------------------------------------------

def test_get_predicted_csat(client, respond):
    respond(payloads.PREDICTED_CSAT)
    result = client.call.get_predicted_csat(5237603)
    assert client.session.last["url"] == f"{BASE}/calls/5237603/predicted_csat"
    assert result["csat"]["score"] == 75


def test_get_custom_summary_result(client, respond):
    respond({"id": 999, "custom_summary": {"name": "BANT"}})
    client.call.get_custom_summary_result(812)
    assert client.session.last["url"] == f"{BASE}/calls/812/custom_summary_result"


# --- Call query params ---------------------------------------------------

def test_list_calls_forwards_filters(client, respond):
    respond({"calls": [], "meta": payloads.META})
    client.call.list_calls(order="desc", fetch_aiva_conv=True, **{"from": 1584998199})
    params = client.session.last["params"]
    assert params["order"] == "desc"
    assert params["fetch_aiva_conv"] is True
    assert params["from"] == 1584998199


def test_get_call_forwards_fetch_toggles(client, respond):
    respond({"call": payloads.CALL})
    client.call.get(812, fetch_call_timeline=True)
    assert client.session.last["params"] == {"fetch_call_timeline": True}


def test_get_call_without_toggles_sends_no_params(client, respond):
    respond({"call": payloads.CALL})
    client.call.get(812)
    assert client.session.last["params"] is None


# --- Group messages ------------------------------------------------------

def test_send_group_in_conversation(client, respond):
    respond(payloads.GROUP_MESSAGE)
    result = client.message.send_group_in_conversation(
        123, ["+13000000001", "+13000000002"], "hello"
    )
    assert client.session.last["url"] == f"{BASE}/numbers/123/messages/group/native/send"
    assert client.session.last["json"] == {
        "participants": ["+13000000001", "+13000000002"], "body": "hello"
    }
    assert isinstance(result, GroupMessage)
    assert result.participants == ["+13000000001", "+13000000002"]


def test_send_group_skipping_inbox_with_body(client, respond):
    respond(payloads.GROUP_MESSAGE)
    client.message.send_group_skipping_inbox(123, ["+13000000001"], "hello")
    assert client.session.last["url"] == f"{BASE}/numbers/123/messages/group/send"


def test_send_group_skipping_inbox_with_media(client, respond):
    respond(payloads.GROUP_MESSAGE)
    client.message.send_group_skipping_inbox(
        123, ["+13000000001"], media_url=["http://a/b.png"]
    )
    body = client.session.last["json"]
    assert body["mediaUrl"] == ["http://a/b.png"]
    assert "body" not in body


def test_group_send_requires_content(client):
    with pytest.raises(ValueError, match="body or media_url"):
        client.message.send_group_skipping_inbox(123, ["+13000000001"])
    assert client.session.calls == []


# --- WhatsApp ------------------------------------------------------------

def test_whatsapp_in_conversation_uses_external_number(client, respond):
    """This endpoint names the recipient externalNumber, not to."""
    respond(payloads.MESSAGE)
    result = client.message.send_whatsapp_in_conversation(123, "+130", text="hi")
    assert client.session.last["url"] == f"{BASE}/messages/send/whatsapp/native"
    assert client.session.last["json"] == {
        "lineId": 123, "externalNumber": "+130", "text": "hi"
    }
    assert isinstance(result, Message)


def test_whatsapp_skipping_inbox_uses_to(client, respond):
    """The sibling endpoint names the same field to. They are not interchangeable."""
    respond(payloads.MESSAGE)
    client.message.send_whatsapp_skipping_inbox(123, "+130", text="hi")
    assert client.session.last["url"] == f"{BASE}/messages/whatsapp/send"
    assert client.session.last["json"] == {"lineId": 123, "to": "+130", "text": "hi"}


def test_whatsapp_template_send(client, respond):
    respond(payloads.MESSAGE)
    params = {"id": "1234", "body": [{"key": "{{1}}", "value": "Jordan"}]}
    client.message.send_whatsapp_skipping_inbox(123, "+130", template_params=params)
    assert client.session.last["json"]["templateParams"] == params
    assert "text" not in client.session.last["json"]


@pytest.mark.parametrize(
    "kwargs",
    [{}, {"text": "hi", "template_params": {"id": "1"}}],
    ids=["neither", "both"],
)
def test_whatsapp_rejects_ambiguous_content(client, kwargs):
    with pytest.raises(ValueError, match="exactly one of text or template_params"):
        client.message.send_whatsapp_skipping_inbox(123, "+130", **kwargs)
    assert client.session.calls == []


# --- Templates and channel status ---------------------------------------

def test_list_sms_templates(client, respond):
    respond({"templates": [payloads.SMS_TEMPLATE], "meta": payloads.META})
    page = client.message.list_sms_templates(search="order")
    assert client.session.last["url"] == f"{BASE}/sms/templates"
    assert client.session.last["params"]["search"] == "order"
    assert isinstance(page[0], SmsTemplate)


def test_sms_templates_allow_100_per_page(client, respond):
    """This endpoint documents a cap of 100, not the usual 50."""
    respond({"templates": [], "meta": payloads.META})
    client.message.list_sms_templates(per_page=100)
    assert client.session.last["params"]["per_page"] == 100


def test_sms_templates_still_reject_above_their_own_cap(client):
    with pytest.raises(ValueError, match="between 1 and 100"):
        client.message.list_sms_templates(per_page=101)


def test_list_whatsapp_templates_returns_raw_cursor_response(client, respond):
    respond(payloads.WHATSAPP_TEMPLATES)
    result = client.message.list_whatsapp_templates(123, status="APPROVED")
    assert client.session.last["url"] == f"{BASE}/numbers/123/templates"
    assert client.session.last["params"] == {"status": "APPROVED"}
    assert result["pageInfo"]["nextToken"] == 10


def test_get_whatsapp_status(client, respond):
    respond(payloads.WHATSAPP_STATUS)
    status = client.message.get_whatsapp_status(123)
    assert client.session.last["url"] == f"{BASE}/numbers/123/whatsapp_status"
    assert isinstance(status, WhatsAppLineStatus)
    assert status.canSendMessage is True


# --- AI Voice Agent ------------------------------------------------------

def test_trigger_outbound_call(client, respond):
    respond(payloads.OUTBOUND_CALL)
    result = client.ai_voice_agent.trigger_outbound_call(
        "agent-abc123",
        contact_phone="+15551234567",
        idempotency_key="appt-1",
        context={"first_name": "Jane"},
        expiration_seconds=3600,
    )
    assert client.session.last["url"] == f"{BASE}/outbound-calls/agents/agent-abc123"
    assert client.session.last["json"] == {
        "contact_phone": "+15551234567",
        "idempotency_key": "appt-1",
        "context": {"first_name": "Jane"},
        "expiration_seconds": 3600,
    }
    assert isinstance(result, OutboundCallRequest)
    assert result.status == "PENDING"


def test_outbound_call_omits_unset_optionals(client, respond):
    respond(payloads.OUTBOUND_CALL)
    client.ai_voice_agent.trigger_outbound_call("a", "+1555", "key-1")
    assert client.session.last["json"] == {
        "contact_phone": "+1555", "idempotency_key": "key-1"
    }


@pytest.mark.parametrize("bad", [59, 86401])
def test_outbound_call_validates_expiration(client, bad):
    with pytest.raises(ValueError, match="between 60 and 86400"):
        client.ai_voice_agent.trigger_outbound_call(
            "a", "+1555", "key-1", expiration_seconds=bad
        )
    assert client.session.calls == []


# --- Analytics -----------------------------------------------------------

def test_create_export_with_relative_range(client, respond):
    respond(payloads.ANALYTICS_EXPORT_PENDING)
    result = client.analytics.create_export(
        "CALLS_HISTORY", timezone="Europe/Paris", relative_range="LAST_WEEK"
    )
    assert client.session.last["url"] == f"{BASE}/analytics/report/export"
    body = client.session.last["json"]["input"]
    assert body["reportName"] == "CALLS_HISTORY"
    assert body["filter"]["dateFilter"] == {"relative": "LAST_WEEK"}
    assert body["filter"]["timezone"] == "Europe/Paris"
    assert isinstance(result, AnalyticsExport)
    assert result.is_pending


def test_create_export_with_absolute_range_and_filters(client, respond):
    respond(payloads.ANALYTICS_EXPORT_PENDING)
    client.analytics.create_export(
        "CALLS_HISTORY",
        timezone="Europe/Paris",
        absolute_range={"fromDate": "2026-05-01", "toDate": "2026-05-15"},
        filters={"teamIDs": [4242], "withVoicemail": False},
        options={"dateBreakdown": "DAILY"},
        export_options={"format": "CSV"},
    )
    body = client.session.last["json"]["input"]
    assert body["filter"]["dateFilter"]["absoluteRange"]["fromDate"] == "2026-05-01"
    assert body["filter"]["teamIDs"] == [4242]
    assert body["options"] == {"dateBreakdown": "DAILY"}
    assert body["exportOptions"] == {"format": "CSV"}


def test_create_export_rejects_unknown_report(client):
    with pytest.raises(ValueError, match="report_name must be one of"):
        client.analytics.create_export("NOT_A_REPORT", timezone="UTC",
                                       relative_range="TODAY")
    assert client.session.calls == []


@pytest.mark.parametrize(
    "kwargs",
    [
        {},
        {"relative_range": "TODAY",
         "absolute_range": {"fromDate": "2026-05-01", "toDate": "2026-05-02"}},
    ],
    ids=["neither", "both"],
)
def test_create_export_requires_exactly_one_date_range(client, kwargs):
    with pytest.raises(ValueError, match="exactly one of relative_range"):
        client.analytics.create_export("CALLS_HISTORY", timezone="UTC", **kwargs)
    assert client.session.calls == []


def test_create_export_rejects_unknown_relative_range(client):
    with pytest.raises(ValueError, match="relative_range must be one of"):
        client.analytics.create_export("CALLS_HISTORY", timezone="UTC",
                                       relative_range="LAST_FORTNIGHT")


def test_get_export_while_pending(client, respond):
    respond(payloads.ANALYTICS_EXPORT_PENDING)
    export = client.analytics.get_export("9d3f2a1e")
    assert client.session.last["url"] == f"{BASE}/analytics/report/export/9d3f2a1e"
    assert export.is_pending and not export.is_complete
    assert export.downloadUrl is None


def test_get_export_when_complete(client, respond):
    respond(payloads.ANALYTICS_EXPORT_COMPLETE)
    export = client.analytics.get_export("9d3f2a1e")
    assert export.is_complete
    assert export.downloadUrl.endswith("x.csv")
    assert export.downloadUrlExpiresAt is not None


def test_get_export_when_failed(client, respond):
    respond(payloads.ANALYTICS_EXPORT_FAILED)
    export = client.analytics.get_export("9d3f2a1e")
    assert export.is_failed
    assert "too many rows" in export.errorMessage
