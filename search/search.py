"""Module containing code to search for objects within a stream."""
from __future__ import annotations

from typing import Optional

import cv2
from simple_repr import SimpleRepr

from .arduino import Arduino
from .settings import Config


class Search(SimpleRepr):
    """Search a stream for objects."""

    def __init__(self, config: Config, arduino: Optional[Arduino] = None) -> Search:
        """
        # Search.

        Search for objects in a video stream or image.

        Args:
            config: Config
                The Config object representing your
                configuraton file.

            arduino: Optional[Arduino]
                The Arduino object representing your
                Arduino connection if you are using
                an Arduino microcontroller.
        """
        self.arduino = arduino
        self.config = config
        self.center_height = 0
        self.center_width = 0

    def _initialise_camera(self) -> cv2.VideoCapture:
        """Initialise the user's camera based on configuration."""
        stream = cv2.VideoCapture(self.config.camera.index)
        stream.set(3, self.config.window.width)
        stream.set(4, self.config.window.height)
        return stream

    def _search(
        self,
        image: cv2.Mat,
        draw_center: bool = False,
    ) -> list[tuple[int, int, int, int]]:
        """
        Search an image for objects.

        Objects are defined by a haar
        cascade file, path is selected
        using the config.yml file.

        Args:
            image: cv2.Mat
                The image to search.

            draw_center: bool
                Whether to draw the
                center point of the
                screen or not.
        """
        (screen_height, screen_width) = image.shape[:2]
        self.center_height = screen_height // 2
        self.center_width = screen_width // 2

        if draw_center:
            cv2.circle(
                img=image,
                center=(self.center_width, self.center_height),
                radius=7,
                color=(255, 255, 255),
                thickness=-1,
            )

        # Grayscale image for better detection
        gray_img = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2GRAY,
        )

        # Get all objects found.
        objects = self.config.cascade.detectMultiScale(
            gray_img,
            1.1,
            4,
        )

        return objects

    def _draw_objects(
        self,
        image: cv2.Mat,
        draw_center: bool = False,
    ) -> list[tuple[int, int]]:
        """
        Highlight all objects found in an image on screen.

        Args:
            image: cv2.Mat
                The image searched to locate the objects.

            draw_center:
                Whether to draw the center point of each
                object found on screen or not.

        Returns:
            The centerpoint of each object's x and y
            coordinates on the screen.
        """
        object_coordinates = []

        for (x, y, w, h) in self._search(image=image, draw_center=draw_center):
            cv2.rectangle(
                img=image,
                pt1=(x, y),
                pt2=(x + w, y + h),
                color=(0, 0, 255),
                thickness=2,
            )

            rect_center_x = (x + (x + w)) // 2
            rect_center_y = (y + (y + h)) // 2

            if draw_center:
                cv2.circle(
                    img=image,
                    center=(rect_center_x, rect_center_y),
                    radius=7,
                    color=(0, 0, 255),
                    thickness=-1,
                )
            object_coordinates.append(
                (rect_center_x, rect_center_y),
            )

        cv2.imshow("Detection", image)
        return object_coordinates

    def _set_stream(self) -> cv2.VideoCapture | None:
        """Set a video stream if the user has chosen to use a camera."""
        stream = None

        if self.config.camera.use:
            stream = self._initialise_camera()

        return stream

    def _set_image(self) -> cv2.Mat | None:
        """Set an image if the user has chosen to use an image."""
        image = None

        if self.config.image.use:
            image = cv2.imread(self.config.image.path)

        return image

    def _iterate_objects(
        self,
        image: Optional[cv2.Mat] = None,
        stream: Optional[cv2.VideoCapture] = None,
        draw_center: bool = False,
    ) -> None:
        """
        Iterate over objects found in an image or video stream.

        Args:
            image: Optional[cv2.Mat]
                An image to search for objects.

            stream: Optional[cv2.VideoCapture]
                A video stream to search for objects.

            draw_center: bool
                Whether to draw the centerpoint of the
                screen, and center points of each object.

        Raises: ValueError
            If more than one media type is passed in.
        """
        if image is None and stream is None:
            raise ValueError("No image or stream provided.")

        while True:
            if stream:
                _, image = stream.read()

            objects = self._draw_objects(
                image=image,
                draw_center=draw_center,
            )

            if self.arduino:
                for (rect_center_x, rect_center_y) in objects:
                    self.arduino.aim(
                        x=rect_center_x,
                        y=rect_center_y,
                        h=self.center_height,
                        w=self.center_width,
                        offset=self.config.offset,
                    )

            if not stream or cv2.waitKey(1) & 0xFF == ord("q"):
                break

    def run(self, draw_centers: bool = False) -> None:
        """
        Search an image or video stream for defined objects.

        Object definitions are provided to the program via
        haar cascades located in the resources folder.

        Args:
            draw_centers: bool
                Whether to draw the centerpoint of the
                screen, and center points of each object.

        Raises: ValueError
            If the config file says to use more than
            one media type.
        """
        if self.config.camera.use and self.config.image.use:
            raise ValueError("Cannot use both camera and image.")

        stream = self._set_stream()
        image = self._set_image()

        self._iterate_objects(
            image=image,
            stream=stream,
            draw_center=draw_centers,
        )

        if self.config.image.use:
            cv2.waitKey(0)

        cv2.destroyAllWindows()
