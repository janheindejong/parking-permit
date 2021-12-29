import pytest

from parking_permit.agent import QueueEntry


@pytest.fixture
def html_response() -> str:
    with open("tests/html_response.txt", "r") as f:
        data = f.read()
    return data


@pytest.fixture
def license_plate() -> str:
    return "AB-123-CD"


@pytest.fixture
def client_number() -> str:
    return "1234567"


@pytest.fixture
def recipient_address() -> str:
    return "john@doe.com"


@pytest.fixture
def entry(
    license_plate: str,
    html_response: str,
) -> QueueEntry:
    entry = QueueEntry(license_plate, "West-1.1", 42, html_response)
    return entry
