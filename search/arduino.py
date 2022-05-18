"""Manage connection and interfacing with Arduino."""
from __future__ import annotations

from serial import Serial


class Arduino:
    """Interface with Arduino."""

    def __init__(
        self,
        port: str,
        baudrate: int = 115200,
        timeout: float = 0.1,
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

            offset: int
                The ammount of padding in pixels
                to allow for the Arduino to consider
                the object centered.
        """
        directions = ""

        if x <= w - offset:
            # Too far right
            directions += "L"

        if x >= w + offset:
            # Too far left
            directions += "R"

        if y <= h - offset:
            # Too high
            directions += "U"

        if y >= h + offset:
            # Too low
            directions += "D"

        else:
            # Centered
            directions = "C"

        self.write(directions)
