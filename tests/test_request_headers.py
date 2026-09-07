"""The headers the SDK actually puts on the wire.

The shared `client` fixture swaps the whole requests.Session out, so nothing in
the suite ever saw an outgoing header. That blind spot hid a real bug: requests
only sets Content-Type when it serialises a body, so every GET left the SDK
without one, and the two endpoints that require it -- registration_status and
messages/configuration -- returned 400 InvalidContentType for the life of the
SDK. These tests keep a real Session and capture the prepared request.
"""

import json as jsonlib

import pytest
import requests
from requests.adapters import HTTPAdapter

from aircall import AircallClient
from tests import payloads


class CapturingAdapter(HTTPAdapter):
    """Transport that records the prepared request instead of sending it."""

    def __init__(self, payload):
        super().__init__()
        self.payload = payload
        self.sent = None

    def send(self, request, **kwargs):
        self.sent = request
        response = requests.Response()
        response.status_code = 200
        response.request = request
        response._content = jsonlib.dumps(self.payload).encode()
        response.encoding = "utf-8"
        return response


@pytest.fixture
def wire():
    """A client on a real Session, plus the adapter that captured the request."""
    def _wire(payload=None):
        client = AircallClient(api_id="test_id", api_token="test_token")
        adapter = CapturingAdapter(payload if payload is not None else {})
        client.session.mount("https://", adapter)
        return client, adapter

    return _wire


def test_get_carries_a_json_content_type(wire):
    """GET /numbers/{id}/registration_status 400s without this header."""
    client, adapter = wire({"registration_status": "verified"})
    client.number.get_registration_status(123)
    assert adapter.sent.headers["Content-Type"] == "application/json"


def test_message_configuration_get_carries_a_json_content_type(wire):
    """The other endpoint that rejects a bodyless request without it."""
    client, adapter = wire({"configuration": {}})
    client.message.get_configuration(123)
    assert adapter.sent.headers["Content-Type"] == "application/json"


def test_plain_get_still_carries_the_header(wire):
    """Endpoints that tolerate a missing Content-Type must not regress either."""
    client, adapter = wire({"numbers": [payloads.NUMBER], "meta": payloads.META})
    client.number.list_numbers()
    assert adapter.sent.headers["Content-Type"] == "application/json"


def test_post_body_is_unchanged_by_the_session_header(wire):
    """Setting Content-Type session-wide must not disturb serialised bodies."""
    client, adapter = wire(payloads.MESSAGE)
    client.message.send_skipping_inbox(123, "+130", "hello")
    assert adapter.sent.headers["Content-Type"] == "application/json"
    assert jsonlib.loads(adapter.sent.body) == {"to": "+130", "body": "hello"}


def test_authorization_survives_alongside_the_content_type(wire):
    client, adapter = wire({"ping": "pong"})
    client.ping()
    assert adapter.sent.headers["Authorization"].startswith("Basic ")
