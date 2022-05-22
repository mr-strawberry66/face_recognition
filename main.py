"""Module for searching for objects within a stream."""
from serial.serialutil import SerialException

from search import Arduino, Config, RaspberryPi, Search


def main(path: str):
    """
    Search for objects in a video or image.

    path: str
        The path to your config file.
    """
    config = Config.from_file(path)
    arduino = None
    raspberry_pi = None

    try:
        arduino = Arduino(port=config.port)
    except SerialException:
        print("Could not connect to Arduino.\nRunning without connection.")

    try:
        raspberry_pi = RaspberryPi(14, 15)
    except RuntimeError:
        print("Not running on a RPi")

    Search(arduino=arduino, ras_pi=raspberry_pi, config=config).run()


if __name__ == "__main__":
    main("config.yml")
