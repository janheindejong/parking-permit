import pytest

from parking_permit.agent import QueueEntry
from parking_permit.html_parser import HtmlParser


@pytest.fixture
def html_parser() -> HtmlParser:
    return HtmlParser()


@pytest.fixture
def entry(html_parser: HtmlParser, html_response: str) -> QueueEntry:
    return html_parser.parse(html_response)


def test_license_plate(entry: QueueEntry):
    assert entry.license_plate == "AB-123-CD"


def test_position(entry: QueueEntry):
    assert entry.position == 42


def test_area(entry: QueueEntry):
    assert entry.area == "West-1.1"
