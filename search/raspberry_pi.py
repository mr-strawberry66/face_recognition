"""Class to control Raspberry Pi pins."""
from __future__ import annotations

from .rpi.servo import Servo


class RaspberryPi:
    """Interface with a Raspberry Pi."""

    def __init__(
        self,
        servo_x_pin: int,
        servo_y_pin: int,
        movement_amount: int = 10,
    ) -> RaspberryPi:
        """
        # Raspberry Pi.

        Control the camera using a Raspberry Pi.

        Args:
            servo_x_pin: int
                The pin number connected to the
                servo controlling x-axis movement

            servo_y_pin: int
                The pin number connected to the
                servo controlling y-axis movement

            movement_amount: int
                The amount to move each servo
                when making adjustments. Default
                is 10.
        """
        self.servo_x = Servo(servo_x_pin)
        self.servo_y = Servo(servo_y_pin, max_degree=150)
        self.movement_amount = movement_amount

    def aim(
        self,
        x: int,
        y: int,
        h: int,
        w: int,
        offset: int,
    ) -> str:
        """
        Aim the camera.

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
                to allow for the Raspberry Pi to
                consider the object centered.
        """
        if x < w - offset:
            # Too far left
            self.servo_x.set_angle(self.servo_x.current_angle + self.movement_amount)

        elif x > w + offset:
            # Too far right
            self.servo_x.set_angle(self.servo_x.current_angle - self.movement_amount)

        if y <= h - offset:
            # Too low
            self.servo_y.set_angle(self.servo_y.current_angle - self.movement_amount)

        elif y > h + offset:
            # Too high
            self.servo_y.set_angle(self.servo_y.current_angle + self.movement_amount)
