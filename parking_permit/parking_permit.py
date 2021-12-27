import re
from typing import Union

import requests

URL = (
    "https://www.amsterdam.nl/parkeren-verkeer/parkeervergunning/"
    + "parkeervergunning-bewoners/wachtlijst/"
    + "?module=16349201&ajax=true&rich-ajax=true"
)


class Client:
    def __init__(self, license_plate: str, client_number: Union[int, str]) -> None:
        self.license_plate: str = license_plate
        self.client_number: str = str(client_number)

    def get_current_position(self) -> int:
        response = self.send_request()
        return self.parse_response_text(response.text)

    def send_request(self) -> requests.Response:
        with requests.Session() as client:
            response = client.get(URL, params=self.get_params())
        return response

    def parse_response_text(self, text: str) -> int:
        # TODO fix regex
        m = re.match(
            "<h3 class=label>Huidige wachtlijstpositie</h3>"
            + " <p class=value>9</p>"
            + " <h3 class=label>Verwachte uitgiftedatum</h3>",
            text,
        )
        return 0

    def get_params(self):
        return {"kenteken": self.license_plate, "klantnummer": self.client_number}
