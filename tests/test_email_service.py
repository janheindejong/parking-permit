import pytest

from parking_permit.mail_service import MailService

MESSAGE = "Hello, world!"


@pytest.fixture
def service() -> MailService:
    service = MailService("test-account@host.com", "p@ssw0rd", "smtp.host.com")
    return service


def test_email_sent(service: MailService):
    service.send("recipient@recepienthost.com", "Hello, world!")
