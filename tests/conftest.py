"""Shared fixtures for the Aircall SDK test suite.

Tests never touch the network. A recording stand-in replaces the client's
requests.Session, so the full _request path -- URL construction, version
routing, status handling, model parsing -- runs exactly as it does in
production, with the response payload supplied by the test.
"""

import pytest

from aircall import AircallClient


class FakeResponse:
    """Minimal stand-in for requests.Response."""

    def __init__(self, payload, status_code=200, headers=None):
        self._payload = payload
        self.status_code = status_code
        self.reason = "OK" if status_code < 400 else "Error"
        self.headers = headers or {}
        self.text = ""

    def json(self):
        return self._payload


class RecordingSession:
    """Stand-in for requests.Session that records calls and replays a payload."""

    def __init__(self):
        self.calls = []
        self.payload = {}
        self.status_code = 200
        self.headers = {}

    # Matches the keyword arguments AircallClient._request passes.
    def request(self, method, url, params=None, json=None, timeout=None):
        self.calls.append(
            {"method": method, "url": url, "params": params, "json": json,
             "timeout": timeout}
        )
        return FakeResponse(self.payload, self.status_code, self.headers)

    @property
    def last(self):
        """The most recent recorded call."""
        assert self.calls, "no request was made"
        return self.calls[-1]


@pytest.fixture
def client():
    """An AircallClient whose transport is a RecordingSession."""
    api_client = AircallClient(api_id="test_id", api_token="test_token")
    api_client.session = RecordingSession()
    return api_client


@pytest.fixture
def respond(client):
    """Set the payload the next request will return."""

    def _respond(payload, status_code=200, headers=None):
        client.session.payload = payload
        client.session.status_code = status_code
        client.session.headers = headers or {}

    return _respond
