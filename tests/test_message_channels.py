"""The two message send channels, and the deprecated names for them.

send() used to mean "skip the agent inbox" while send_native() meant the
opposite of what its name suggested, and send_native()'s docstring wrongly
described it as a WhatsApp template endpoint. Getting these the wrong way round
routes customer traffic down the wrong channel, so the old names still work but
warn.
"""

import pytest

from aircall.models import Message

from tests import payloads

IN_CONVERSATION = "https://api.aircall.io/v1/numbers/123/messages/native/send"
SKIPPING_INBOX = "https://api.aircall.io/v1/numbers/123/messages/send"


def test_send_in_conversation_targets_the_native_endpoint(client, respond):
    respond(payloads.MESSAGE)
    message = client.message.send_in_conversation(123, "+130", "hello")
    assert client.session.last["url"] == IN_CONVERSATION
    assert client.session.last["json"] == {"to": "+130", "body": "hello"}
    assert isinstance(message, Message)


def test_send_skipping_inbox_targets_the_plain_endpoint(client, respond):
    respond(payloads.MESSAGE)
    client.message.send_skipping_inbox(123, "+130", "hello")
    assert client.session.last["url"] == SKIPPING_INBOX


def test_media_url_is_sent_camel_cased(client, respond):
    """Aircall expects mediaUrl, not media_url."""
    respond(payloads.MESSAGE)
    client.message.send_skipping_inbox(123, "+130", "hi", media_url=["http://a/b.png"])
    assert client.session.last["json"]["mediaUrl"] == ["http://a/b.png"]


def test_media_url_omitted_when_not_given(client, respond):
    respond(payloads.MESSAGE)
    client.message.send_skipping_inbox(123, "+130", "hi")
    assert "mediaUrl" not in client.session.last["json"]


def test_deprecated_send_warns_and_skips_the_inbox(client, respond):
    respond(payloads.MESSAGE)
    with pytest.warns(DeprecationWarning, match="skips the Aircall inbox"):
        client.message.send(123, "+130", "hi")
    assert client.session.last["url"] == SKIPPING_INBOX


def test_deprecated_send_native_warns_and_uses_the_conversation(client, respond):
    respond(payloads.MESSAGE)
    with pytest.warns(DeprecationWarning, match="agent conversation"):
        client.message.send_native(123, to="+130", body="hi")
    assert client.session.last["url"] == IN_CONVERSATION


def test_deprecated_names_still_return_a_parsed_message(client, respond):
    respond(payloads.MESSAGE)
    with pytest.warns(DeprecationWarning):
        assert isinstance(client.message.send(123, "+130", "hi"), Message)


def test_configuration_endpoints_are_unchanged(client, respond):
    respond({"token": "t", "callbackUrl": "http://x", "type": "Public Api"})
    client.message.create_configuration(123, callbackUrl="http://x", type="whatsapp")
    assert client.session.last["url"].endswith("/numbers/123/messages/configuration")
    assert client.session.last["json"]["type"] == "whatsapp"
