"""Authentication schemes and the credential check endpoint.

Aircall customers authenticate with Basic Auth; technology partners use OAuth
2.0 Bearer tokens. Only Basic was supported, which left partner integrations
unable to use the SDK at all.
"""

import base64

import pytest

from aircall import AircallClient


def test_basic_auth_header():
    client = AircallClient(api_id="my_id", api_token="my_token")
    expected = base64.b64encode(b"my_id:my_token").decode()
    assert client.session.headers["Authorization"] == f"Basic {expected}"


def test_oauth_bearer_header():
    client = AircallClient(access_token="oauth_token_123")
    assert client.session.headers["Authorization"] == "Bearer oauth_token_123"


def test_no_credentials_is_rejected():
    with pytest.raises(ValueError, match="Authentication required"):
        AircallClient()


@pytest.mark.parametrize("kwargs", [{"api_id": "only_id"}, {"api_token": "only_token"}])
def test_partial_basic_credentials_are_rejected(kwargs):
    with pytest.raises(ValueError, match="Authentication required"):
        AircallClient(**kwargs)


def test_mixing_both_schemes_is_rejected():
    """Ambiguous intent; Aircall accepts one Authorization header, not two."""
    with pytest.raises(ValueError, match="not both"):
        AircallClient(api_id="i", api_token="t", access_token="a")


def test_positional_basic_auth_still_works():
    """The 1.x calling convention must not break."""
    client = AircallClient("my_id", "my_token")
    assert client.session.headers["Authorization"].startswith("Basic ")


def test_ping_targets_the_v1_endpoint(client, respond):
    respond({"ping": "pong"})
    assert client.ping() == {"ping": "pong"}
    assert client.session.last["url"] == "https://api.aircall.io/v1/ping"
    assert client.session.last["method"] == "GET"
