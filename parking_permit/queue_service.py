import requests
from requests import Request, Response

from .agent import QueueEntry, QueueServiceProtocol

URL = (
    "https://www.amsterdam.nl/parkeren-verkeer/parkeervergunning/"
    + "parkeervergunning-bewoners/wachtlijst/"
)


class QueueService(QueueServiceProtocol):
    def __init__(self) -> None:
        self._session = requests.Session()

    def get_queue_entry(self, license_plate: str, client_number: str) -> QueueEntry:
        response = self._get_response(license_plate, client_number)
        entry = self._parse_response(license_plate, client_number, response)
        return entry

    def _get_response(self, license_plate: str, client_number: str) -> Response:
        request = self._build_request(license_plate, client_number)
        response = self._send_request(request)
        return response

    def _parse_response(
        self, license_plate: str, client_number: str, response: Response
    ) -> QueueEntry:
        # TODO actual parsing, not just HTML
        entry = QueueEntry(
            license_plate=license_plate,
            client_number=client_number,
            area="",
            position=0,
            html=response.text,
        )
        return entry

    def _build_request(
        self, license_plate: str, client_number: str
    ) -> requests.Request:
        request = Request(
            "GET",
            url=URL,
            params={
                "kenteken": license_plate,
                "klantnummer": client_number,
                "module": 16349201,
                "ajax": "true",
                "rich-ajax": "true",
            },
        )
        return request

    def _send_request(self, request: Request) -> Response:
        with self._session as s:
            prepped = s.prepare_request(request)
            response = s.send(prepped)
        return response
