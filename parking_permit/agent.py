import dataclasses
import logging
from abc import abstractmethod
from typing import Protocol

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class QueueEntry:

    license_plate: str
    client_number: str
    area: str
    position: int
    html: str


class MailServiceProtocol(Protocol):
    @abstractmethod
    def send(self, to: str, entry: QueueEntry) -> None:
        ...


class QueueServiceProtocol(Protocol):
    @abstractmethod
    def get_queue_entry(self, license_plate: str, client_number: str) -> QueueEntry:
        ...


class ParkingPermitAgent:
    """Monitors pos ition in parking permit queue"""

    def __init__(
        self,
        license_plate: str,
        client_number: str,
        recipient_address: str,
        queue_service: QueueServiceProtocol,
        mail_service: MailServiceProtocol,
    ) -> None:
        self._license_plate: str = license_plate
        self._client_number: str = client_number
        self._recipient_address: str = recipient_address
        self._queue_service: QueueServiceProtocol = queue_service
        self._mail_service: MailServiceProtocol = mail_service

    def run_once(self):
        entry = self._get_queue_entry()
        logger.debug(entry)
        self._mail_service.send(self._recipient_address, entry)

    def _get_queue_entry(self) -> QueueEntry:
        return self._queue_service.get_queue_entry(
            self._license_plate, self._client_number
        )
