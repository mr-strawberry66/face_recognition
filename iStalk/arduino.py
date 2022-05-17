"""Manage connection and interfacing with Arduino"""
from __future__ import annotations

from serial import Serial


class Arduino:
    """Interface with Arduino."""

    def __init__(
        self,
        port: str,
        baudrate: int = 115200,
        timeout: int = 0.1,
    ) -> Arduino:
        """
        # Arduino.

        Interface with an Arduino.

        Args:
            port: str
                The port used by the Arduino
                microcontroller.

            baudrate: int
                The baudrate set onboard
                the Arduino.

            timeout: int
                How long to wait before
                allowing the connection
                to timeout (seconds).
        """
        self.connection = Serial(
            port=port,
            baudrate=baudrate,
            timeout=timeout,
        )

    def write(self, data: str) -> None:
        """Post data to the Arduino."""
        self.connection.write(data.encode("utf-8"))

    def aim(
        self,
        x: int,
        y: int,
        h: int,
        w: int,
        offset: int,
    ) -> None:
        """
        Aim the Arduino mounted camera.

        Args:
            x: int
                The x coordinate of the center
                of the object to track.

            y: int
                The y coordinate of the center
                of the object to track.

            h: int
                The camera centerpoint's height.

            w: int
                The camera centerpoint's width.
        """
        if int(y) >= int(h) + offset and int(x) >= int(w) + offset:
            # Too low and too far left
            self.write("1")

        elif int(y) >= int(h) + offset and int(x) <= int(w) - offset:
            # Too low and too far right
            self.write("2")

        elif int(y) <= int(h) - offset and int(x) >= int(w) + offset:
            # Too high and too far left
            self.write("3")

        elif int(y) <= int(h) - offset and int(x) <= int(w) - offset:
            # Too high and too far right
            self.write("4")

        elif int(y) >= int(h) + offset:
            # Too low
            self.write("5")

        elif int(y) <= int(h) - offset:
            # Too high
            self.write("6")

        elif int(x) >= int(w) + offset:
            # Too far left
            self.write("7")

        elif int(x) <= int(w) - offset:
            # Too far right
            self.write("8")

        else:
            # Centered
            self.write("0")
