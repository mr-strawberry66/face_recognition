"""Manage project configuration."""
from __future__ import annotations

import os
from dataclasses import dataclass

import cv2
from simple_repr import SimpleRepr
import yaml


class Config(SimpleRepr):
    """Manage project configuration settings."""

    def __init__(
        self,
        offset: int,
        port: str,
        cascade_name: str,
        camera: dict[str, str],
        image: dict[str, str],
        window: dict[str, str],
    ) -> Config:
        """
        # Config.

        Load existing configurations.

        Args:
            offset: int
                The offset allowed for the
                detection algorithm's accuracy.

            port: str
                The port used by the Arduino
                microcontroller.

            cascade_path: str
                The name of the haar cascade
                to use to define the object(s)
                to track. Store haar cascades
                in the resources folder.

            camera: dict[str, str]
                The settings for the camera.

                Keys:
                    index: int
                        Which camera to use.

                    use: bool
                        Whether to use the camera
                        as the image stream.

            image: dict[str, str]
                The settings for working with an image.

                Keys:
                    path: str
                        The path to the image.

                    use: bool
                        Whether to use the image
                        as the image stream.

            window: dict[str, str]
                The size of the window to open when
                running the code.

                Keys:
                    width: int
                        How wide the window should
                        be in pixels.

                    height: int
                        How tall the window should
                        be in pixels.
        """
        self.offset = offset
        self.port = port
        self.cascade = cv2.CascadeClassifier(
            os.path.join(
                "resources",
                cascade_name,
            )
        )
        self.camera = Camera(
            index=camera["index"],
            use=camera["use"],
        )
        self.image = Image(
            path=image["path"],
            use=image["use"],
        )
        self.window = Window(
            width=window["width"],
            height=window["height"],
        )

    @classmethod
    def from_file(cls, path: str = "") -> Config:
        """
        Load existing config from file or generate a new file.

        Args:
            path: str
                The path to the config file.

        Returns: Config
            The configuration object.
        """
        settings = Settings(path=path)

        if not settings.file_exists():
            settings.create_default()

        return cls(**settings.load())


class Settings(SimpleRepr):
    """Load project configuration settings."""

    def __init__(self, path: str = "") -> Settings:
        """
        # Settings.

        Operations to load and store configs.

        Args:
            path: str
                The path to the config file
                to load or create.
        """
        self.path = path or "config.yml"
        self.defaults = {
            "offset": 50,
            "port": "COM3",
            "cascade_name": "face.xml",
            "camera": {
                "index": 0,
                "use": True,
            },
            "image": {
                "path": "",
                "use": False,
            },
            "window": {
                "width": 1920,
                "height": 1080,
            },
        }

    def file_exists(self) -> bool:
        """Return whether the config file exists or not."""
        return os.path.exists(self.path)

    def create_default(self) -> None:
        """Create the default config file."""
        with open(self.path, "w") as file:
            yaml.dump(self.defaults, file)

    def load(self) -> dict[str, str | int | dict[str, str | int | bool]]:
        """Load the config file."""
        with open(self.path, "r") as file:
            data = yaml.safe_load(file)

        if not self._is_valid(data):
            self._replace_invalid()
            return self.defaults

        return data

    def _replace_invalid(self):
        """Replace invalid config files with the default settings."""
        os.remove(self.path)
        self.create_default()

    def _is_valid(self, data) -> bool:
        """Test if loaded data is valid."""
        if not data:
            return False

        if set(self.defaults.keys()) != set(data.keys()):
            return False

        return True


@dataclass
class Camera:
    """Camera settings."""

    index: int
    use: bool


@dataclass
class Image:
    """Image settings."""

    path: str
    use: bool


@dataclass
class Window:
    """Window settings."""

    width: int
    height: int
