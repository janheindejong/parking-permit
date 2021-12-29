from abc import abstractmethod
from typing import Protocol


class MailServiceProtocol(Protocol):
    @abstractmethod
    def send(self, to: str, html: str) -> None:
        ...


class QueueServiceProtocol(Protocol):
    @abstractmethod
    def get_queue_entry_html(self, license_plate: str, client_number: str) -> str:
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
        self._license_plate: str = license_plate
        self._client_number: str = client_number
        self._recipient_address: str = recipient_address
        self._queue_service: QueueServiceProtocol = queue_service
        self._mail_service: MailServiceProtocol = mail_service

    def run_once(self):
        html = self._get_html()
        self._mail_service.send(self._recipient_address, html)

    def _get_html(self) -> str:
        return self._queue_service.get_queue_entry_html(
            self._license_plate, self._client_number
        )
