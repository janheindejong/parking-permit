import smtplib
import ssl
from contextlib import contextmanager
from email.message import EmailMessage
from typing import Generator

from .agent import MailServiceProtocol, QueueEntry


class MailService(MailServiceProtocol):
    def __init__(
        self, account: str, password: str, server: str, port: int = 465
    ) -> None:
        self._account = account
        self._password = password
        self._server = server
        self._port = port

    def send(self, recipient: str, entry: QueueEntry) -> None:
        msg = self._build_message(recipient, entry)
        with self._mail_server() as server:
            server.send_message(msg)

    @contextmanager
    def _mail_server(self) -> Generator[smtplib.SMTP_SSL, None, None]:
        # Create a secure SSL context
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL(self._server, self._port, context=context) as server:
            server.login(self._account, self._password)
            yield server

    def _build_message(self, recipient: str, entry: QueueEntry) -> EmailMessage:
        msg = EmailMessage()
        msg["Subject"] = f"Position in parking queue for {entry.license_plate}"
        msg["To"] = recipient
        msg["From"] = self._account
        msg.set_content(entry.html)
        msg.add_alternative(entry.html, subtype="html")
        return msg
