import dataclasses
import logging
import time
from abc import abstractmethod
from typing import Protocol, Union

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class QueueEntry:

    license_plate: str
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
    """Monitors position in parking permit queue"""

    def __init__(
        self,
        license_plate: str,
        client_number: str,
        recipient_address: str,
        queue_service: QueueServiceProtocol,
        mail_service: MailServiceProtocol,
    ) -> None:
        self._license_plate = license_plate
        self._client_number = client_number
        self._recipient_address = recipient_address
        self._queue_service = queue_service
        self._mail_service = mail_service
        self._position: Union[int, None] = None

    def run(self, wait: int):
        while True:
            self.run_once()
            time.sleep(wait)

    def run_once(self):
        entry = self._get_queue_entry()
        logger.debug(f"self={self._position}; entry={entry.position}")
        if (not self._position) or (self._position != entry.position):
            logger.info("Change in position; sending e-mail")
            self._mail_service.send(self._recipient_address, entry)
            self._position = entry.position
        else:
            logger.info("No change in position")

    def _get_queue_entry(self) -> QueueEntry:
        return self._queue_service.get_queue_entry(
            self._license_plate, self._client_number
        )
