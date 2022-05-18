"""Module for searching for objects within a stream."""
from search import Arduino, Config, Search

from serial.serialutil import SerialException


def main(path: str):
    """
    Search for objects in a video or image.

    path: str
        The path to your config file.
    """
    config = Config.from_file(path)
    arduino = None

    try:
        arduino = Arduino(port=config.port)
    except SerialException:
        print("Could not connect to Arduino.\nRunning without connection.")

    Search(arduino=arduino, config=config).run()


if __name__ == "__main__":
    main("config.yml")
