"""Control servos from a Raspberry Pi."""
from __future__ import annotations

import RPi.GPIO as IO

from numpy import interp


class Servo:
    """Control a servo using a Raspberry Pi."""

    def __init__(
        self,
        pin: int,
        min_degree: int = 0,
        max_degree: int = 180,
    ) -> Servo:
        """
        # Servo.

        Control a servo from a Raspberry PI.

        Args:
            pin: int
                The pin number on your Raspberry PI
                that the servo is connected to.

            min_degree: int
                The smallest value in a range to
                enable the servo to rotate to.
                Min is 0.

            max_degree: int
                The largest value in a range to
                enable to servo to rotate to.
                Max is 180.
        """
        IO.setwarnings(False)
        IO.setmode(IO.BCM)
        IO.setup(pin, IO.OUT)

        self.pwm = IO.PWM(pin, 50)
        self.pwm.start(2.5)
        self.min_degree = min_degree
        self.max_degree = max_degree
        self.current_angle = 0

    def __del__(self) -> None:
        """Clean up when class instance is no longer in use."""
        self.pwm.stop()

    def set_angle(self, angle: int) -> None:
        """
        Set the angle of a servo.

        Args:
            angle: int
                The angle (between 0 and 180) to
                set the servo to turn to.
        """
        angle = max(min(angle, self.max_degree), self.min_degree)
        corrected_angle = interp(
            angle,
            [self.min_degree, self.max_degree],
            [25, 125],
        )
        self.pwm.ChangeDutyCycle(round(corrected_angle / 10, 1))
        self.current_angle = angle
