# Object detection
Project to run object detections over images and video streams.


## API
There are 3 main classes included with this project.


### Settings
This class is responsible for handling configuration. On first run, it will generate a `config.yml` file. This can be updated with a number of parameters. You can create a `Config` instance easily by calling the method `Config.from_file()`.

| Parameter | Type | Use |
| --------- | ---- | --- |
| `camera` | `class` | Parent for camera settings. |
| `camera.index` | `int` | Which camera to use if you have more than one camera on your device, defaults to 0 |
| `camera.use` | `bool` | Whether to use a camera as the input stream to search. Note that either this or `image.use` must be true, but not both. |
| `image` | `class` | Parent for image settings. |
| `image.path` | `str` | The path of the image to search |
| `image.use` | `bool` | Whether to use an image as the input stream to search. |
| `cascade_name` | `str` | The file name of the haar cascade to use in the resources folder. |
| `offset` | `int` | For Arduino users running the `tracking.ino` script, this is the amount of pixels to allow as padding between the center of the object you are tracking, and the center of the camera's visible range. |
| `port` | `str` | For Arduino users, set this to the serial port your Arduino is occupying. |

Note that outright deleting any items from your config file will result in it being re-created using the default settings.


### Arduino
This class handles sending the Arduino instructions. If you are not using an Arduino alongside this code, you can ignore this.

| Parameter | Type | Use |
| --------- | ---- | --- |
| `port` | `str` | The serial port your Arduino is using. |
| `baudrate` | `int` | The baudrate to use with your Arduino. Defaults to `115200`. |
| `timeout` | `float` | How long to wait before allowing the connection to time out. Defaults to `0.1` seconds. |


### Search
This class is used to locate objects in your input stream.
| Parameter | Type | Use |
| --------- | ---- | --- |
| `config`  | `Config` | A configuration object generated with `Config.from_file()` or manually instantiated. |
| `arduino` | `Optional[Arduino]` | An instance of the `Arduino` class that is used to send commands to your Arduino microcontroller.


## Example useage
### Without Arduino
```py
def main(path: str) -> None:
    """
    Search for objects in a video or image.

    path: str
        The path to your config file.
    """
    config = Config.from_file(path)
    Search(config=config).run()


if __name__ == "__main__":
    main("config.yml")
```

### With Arduino
```py
def main(path: str) -> None:
    """
    Search for objects in a video or image.

    path: str
        The path to your config file.
    """
    config = Config.from_file(path)
    arduino = Arduino(port=config.port)
    Search(arduino=arduino, config=config).run()


if __name__ == "__main__":
    main("config.yml")
```
