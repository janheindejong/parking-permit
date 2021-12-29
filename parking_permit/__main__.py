import argparse
import logging

from parking_permit.html_parser import HtmlParser
from parking_permit.mail_service import MailService

from .agent import ParkingPermitAgent
from .queue_service import QueueService

# TODO more professional logging; this is rather rudimentary
logging.basicConfig(level=logging.INFO)


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="Parking Permit Queue")
    parser.add_argument("license_plate", type=str)
    parser.add_argument("client_number", type=str)
    parser.add_argument("recipient_address", type=str)
    parser.add_argument("account", type=str)
    parser.add_argument("password", type=str)
    parser.add_argument("--server", dest="server", type=str, default="smtp.gmail.com")
    parser.add_argument("--port", dest="port", type=str, default=465)
    return parser


def main():
    parser = get_parser()
    args = parser.parse_args()
    html_parser = HtmlParser()
    queue_service = QueueService(html_parser)
    mail_service = MailService(args.account, args.password, args.server, args.port)
    agent = ParkingPermitAgent(
        args.license_plate,
        args.client_number,
        args.recipient_address,
        queue_service,
        mail_service,
    )
    agent.run()


if __name__ == "__main__":
    main()
