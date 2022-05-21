"""Test the settings module."""
import os

from ..settings import Camera, Config, Image, Settings, Window

FILE_PATH = "/tmp/settings.yml"

with open(FILE_PATH, "w") as file:
    file.write("")


def test_settings_file_not_exists():
    """Test the file_exists method."""
    assert Settings(path="./false.txt").file_exists is False


def test_settings_file_exists():
    """Test the file_exists method."""
    assert Settings(path=FILE_PATH).file_exists


def test_settings_load():
    """Test the load method."""
    settings = Settings(path=FILE_PATH)
    assert settings.load() == settings.defaults


def test_settings_is_valid():
    """Test the _is_valid method."""
    settings = Settings(path=FILE_PATH)
    assert settings._is_valid(settings.defaults)
    assert settings._is_valid({"test": "test"}) is False


def test_create_default():
    """Test the create_default method."""
    settings = Settings(path=FILE_PATH)
    settings.create_default()
    assert os.path.exists(FILE_PATH)
    assert settings.load() == settings.defaults


def test_config_from_file_exists():
    """Test the Config class."""
    config = Config.from_file(FILE_PATH)
    assert config.offset == 50
    assert config.port == "COM3"
    assert config.camera == Camera(index=0, use=True)
    assert config.image == Image(path="", use=False)
    assert config.window == Window(width=1920, height=1080)


def test_config_from_file_not_exists():
    """Test the Config class."""
    config = Config.from_file("./false.txt")
    assert config.offset == 50
    assert config.port == "COM3"
    assert config.camera == Camera(index=0, use=True)
    assert config.image == Image(path="", use=False)
    assert config.window == Window(width=1920, height=1080)
    os.remove("./false.txt")
