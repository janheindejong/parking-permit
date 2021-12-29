from unittest.mock import MagicMock

import pytest

from parking_permit.agent import *


# Arrange
@pytest.fixture
def queue_service(entry: QueueEntry) -> MagicMock:
    service = MagicMock(spec=QueueServiceProtocol)
    service.get_queue_entry.return_value = entry
    return service


@pytest.fixture
def mail_service() -> MagicMock:
    return MagicMock(spec=MailServiceProtocol)


@pytest.fixture
def agent(
    license_plate: str,
    client_number: str,
    recipient_address: str,
    queue_service: QueueServiceProtocol,
    mail_service: MailServiceProtocol,
):
    return ParkingPermitAgent(
        license_plate, client_number, recipient_address, queue_service, mail_service
    )


class TestAgentRunOnce:

    # Act
    @pytest.fixture(autouse=True)
    def run_once(self, agent: ParkingPermitAgent):
        agent.run_once()

    # Assess
    def test_queue_service_call(
        self, queue_service: MagicMock, license_plate: str, client_number: str
    ):
        queue_service.get_queue_entry.called_once_with(license_plate, client_number)

    def test_mail_service_call(
        self, mail_service: MagicMock, recipient_address: str, entry: QueueEntry
    ):
        mail_service.send.called_once_with(recipient_address, entry)
