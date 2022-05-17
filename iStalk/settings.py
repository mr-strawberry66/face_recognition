"""Manage project configuration."""
from __future__ import annotations

import os

import cv2
import yaml


class Config:
    """Manage project configuration settings."""

    def __init__(self, offset: int, port: str, cascade_name: str, camera=0) -> Config:
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

            camera: int
                Which camera CV2 should access.
                Defaults to 0, the first camera
                found.
        """
        self.offset = offset
        self.port = port
        self.cascade = cv2.CascadeClassifier(
            os.path.join(
                "resources",
                cascade_name,
            )
        )
        self.camera = camera

    @classmethod
    def from_config_file(cls, path: str = "") -> Config:
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
            return cls(**settings.defaults)

        return cls(**settings.load())


class Settings:
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
            "camera": 0,
            "cascade_name": "face.xml",
        }

    def file_exists(self) -> bool:
        """Return whether the config file exists or not."""
        return os.path.exists(self.path)

    def create_default(self) -> None:
        """Create the default config file."""
        with open(self.path, "w") as file:
            yaml.dump(self.defaults, file)

    def load(self) -> dict[str, str | int]:
        """Load the config file."""
        with open(self.path, "r") as file:
            data = yaml.safe_load(file)

        if not self._valid_data(data):
            self._replace_invalid()
            return self.defaults

        return data

    def _replace_invalid(self):
        """Replace invalid config files with the default settings."""
        os.remove(self.path)
        self.create_default()

    def _valid_data(self, data) -> bool:
        """Test if loaded data is valid"""
        if not data:
            return False

        if set(self.defaults.keys()) != set(data.keys()):
            return False

        return True
