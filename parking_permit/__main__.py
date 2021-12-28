import argparse

from .agent import ParkingPermitAgent

LICENSE_PLATE = "NJ-444-D"
CLIENT_NUMBER = 2080009


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="Parking Permit Queue")
    parser.add_argument("license_plate", type=str)
    parser.add_argument("client_number", type=str)
    return parser


def main():
    parser = get_parser()
    args = parser.parse_args()
    agent = ParkingPermitAgent(args.license_plate, args.client_number)
    agent.run()


if __name__ == "__main__":
    main()
