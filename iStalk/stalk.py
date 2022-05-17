import cv2

from .arduino import Arduino
from .settings import Config


def stalk():
    """Run the code to track objects."""
    config = Config.from_config_file()
    arduino = Arduino(port=config.port)

    cap = cv2.VideoCapture(config.camera)
    print("Accessed camera")

    cap.set(3, 1920)
    print("Width set")

    cap.set(4, 1080)
    print("Height set")

    print("Camera enabled")

    while True:
        _, img = cap.read()

        # Get height and width of screen.
        (ch, cw) = img.shape[:2]
        center_height = ch // 2
        center_width = cw // 2

        # Draw the dot in the screen center.
        cv2.circle(
            img=img,
            center=(center_width, center_height),
            radius=7,
            color=(255, 255, 255),
            thickness=-1,
        )

        # Grayscale image for better detection
        gray_img = cv2.cvtColor(
            img,
            cv2.COLOR_BGR2GRAY,
        )

        # Get all objects found.
        objects = config.cascade.detectMultiScale(
            gray_img,
            1.1,
            4,
        )

        # For each object found, draw a box
        # around the object, and aim the
        # Arduino at it.
        for (x, y, w, h) in objects:
            cv2.rectangle(
                img=img,
                pt1=(x, y),
                pt2=(x + w, y + h),
                color=(0, 0, 255),
                thickness=2,
            )

            rect_center_x = (x + (x + w)) // 2
            rect_center_y = (y + (y + h)) // 2

            cv2.circle(
                img=img,
                center=(rect_center_x, rect_center_y),
                radius=7,
                color=(0, 0, 255),
                thickness=-1,
            )

            arduino.aim(
                x=rect_center_x,
                y=rect_center_y,
                h=center_height,
                w=center_width,
                offset=config.offset,
            )

        cv2.imshow("Detection", img)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    stalk()
