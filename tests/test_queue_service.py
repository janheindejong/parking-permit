from unittest.mock import Mock

import pytest
import requests

from parking_permit.queue_service import *

LICENSE_PLATE = "AB-123-C"
CLIENT_NUMBER = "1234567"
URL = (
    "https://www.amsterdam.nl/parkeren-verkeer/parkeervergunning/"
    + "parkeervergunning-bewoners/wachtlijst/"
    # + "?module=16349201&ajax=true&rich-ajax=true"
)
HTML_RESPONSE = "SOME TEXT"


class MockResponse(requests.Response):
    @property
    def text(self):
        return HTML_RESPONSE


@pytest.fixture
def mock_response():
    return MockResponse()


@pytest.fixture
def requests_session_send(monkeypatch: pytest.MonkeyPatch):
    import requests

    mock = Mock()
    monkeypatch.setattr(requests.Session, "send", mock)
    return mock


@pytest.fixture
def requests_session_prepare_request(monkeypatch: pytest.MonkeyPatch):
    import requests

    mock = Mock()
    monkeypatch.setattr(requests.Session, "prepare_request", mock)
    return mock


@pytest.fixture
def service():
    return QueueService()


@pytest.fixture
def service_request(service: QueueService):
    request = service._build_request(LICENSE_PLATE, CLIENT_NUMBER)
    return request


def test_build_request(service_request: Request):
    assert service_request.method == "GET"
    assert service_request.url == URL
    assert service_request.params == {
        "kenteken": LICENSE_PLATE,
        "klantnummer": CLIENT_NUMBER,
        "module": 16349201,
        "ajax": "true",
        "rich-ajax": "true",
    }


def test_send_request(
    service: QueueService,
    requests_session_send: Mock,
    requests_session_prepare_request: Mock,
    mock_response: MockResponse,
    service_request: Request,
):
    requests_session_prepare_request.return_value = service_request
    requests_session_send.return_value = mock_response
    response = service._send_request(service_request)
    requests_session_send.assert_called_with(service_request)
    assert response == mock_response


def test_unpack_response(service: QueueService, mock_response: MockResponse):
    assert service._unpack_response(mock_response) == HTML_RESPONSE
