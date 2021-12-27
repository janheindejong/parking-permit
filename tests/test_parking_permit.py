from unittest.mock import Mock

import pytest
import requests

import parking_permit

LICENSE_PLATE = "AB-123-C"
CLIENT_NUMBER = "1234567"
URL = (
    "https://www.amsterdam.nl/parkeren-verkeer/parkeervergunning/"
    + "parkeervergunning-bewoners/wachtlijst/"
    + "?module=16349201&ajax=true&rich-ajax=true"
)


class MockResponse(requests.Response):
    @property
    def text(self):
        return "HTML RESPONSE"


@pytest.fixture
def requests_session_get(monkeypatch: pytest.MonkeyPatch):
    import requests

    requests_session_get = Mock()
    monkeypatch.setattr(requests.Session, "get", requests_session_get)
    requests_session_get.return_value = MockResponse()
    return requests_session_get


@pytest.fixture
def client(requests_session_get: Mock):
    return parking_permit.Client(LICENSE_PLATE, CLIENT_NUMBER)


def test_get_params(client: parking_permit.Client):
    assert client.get_params() == {
        "kenteken": LICENSE_PLATE,
        "klantnummer": CLIENT_NUMBER,
    }


def test_send_request(client: parking_permit.Client, requests_session_get: Mock):
    client.send_request()
    requests_session_get.assert_called_once_with(URL, params=client.get_params())


def test_send_request_return(client: parking_permit.Client):
    assert isinstance(client.send_request(), MockResponse)


def test_parse_result(client: parking_permit.Client):
    assert client.parse_response_text("HTML RESPONSE") == 42
