from .queue_service import QueueService


class ParkingPermitAgent:
    """Monitors position in parking permit queue"""

    def __init__(self, license_plate: str, client_number: str) -> None:
        self._license_plate: str = license_plate
        self._client_number: str = client_number
        self._queue_service: QueueService = QueueService()

    def run(self):
        page = self.get_full_page()
        print(page)

    def get_full_page(self) -> str:
        return self._queue_service.get_queue_information(
            self._license_plate, self._client_number
        )
