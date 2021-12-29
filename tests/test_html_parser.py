import pytest

from parking_permit.html_parser import HtmlParser


@pytest.fixture
def html_parser():
    return HtmlParser()
