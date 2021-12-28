import abc
import typing

import requests
from requests import Request, Response

URL = (
    "https://www.amsterdam.nl/parkeren-verkeer/parkeervergunning/"
    + "parkeervergunning-bewoners/wachtlijst/"
)


class ResponseProtocol(typing.Protocol):
    @abc.abstractproperty
    def text(self) -> str:
        ...


class QueueService:
    def __init__(self) -> None:
        self._session = requests.Session()

    def get_queue_information(self, license_plate: str, client_number: str) -> str:
        request = self._create_request(license_plate, client_number)
        response = self._send_request(request)
        return response.text

    def _create_request(
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

    def _parse_response(self, response: ResponseProtocol):
        return response.text
