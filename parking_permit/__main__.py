from .parking_permit import Client

LICENSE_PLATE = "NJ-444-D"
CLIENT_NUMBER = 2080009


def main():
    client = Client(LICENSE_PLATE, CLIENT_NUMBER)
    position = client.get_current_position()
    print(f"Current position in queue: {position}")


if __name__ == "__main__":
    main()
