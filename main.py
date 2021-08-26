import cv2
import os
import time
from serial import Serial

OFFSET = int(os.environ["ACCURACY_OFFSET"])
PORT = os.environ["PORT"]

ARDUINO = Serial(port=PORT, baudrate=115200, timeout=0.1)

CASCADE_PATH = os.path.join("resources", "haarcascade_frontalface_default.xml")
CASCADE = cv2.CascadeClassifier(CASCADE_PATH)


def main():
    cap = cv2.VideoCapture(0)
    print("Accessed camera")

    cap.set(3, 1920)
    print("Width set")

    cap.set(4, 1080)
    print("Height set")

    print("Camera enabled")

    while True:
        success, img = cap.read()
        (ch, cw) = img.shape[:2]
        center_height = ch // 2
        center_width = cw // 2
        circ = cv2.circle(
            img=img,
            center=(center_width, center_height),
            radius=7,
            color=(255, 255, 255),
            thickness=-1,
        )

        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = CASCADE.detectMultiScale(gray_img, 1.1, 4)

        for (x, y, w, h) in faces:
            rect = cv2.rectangle(
                img=img,
                pt1=(x, y),
                pt2=(x + w, y + h),
                color=(0, 0, 255),
                thickness=2,
            )

            rect_center_x = (x + (x + w)) // 2
            rect_center_y = (y + (y + h)) // 2

            rect_center = cv2.circle(
                img=img,
                center=(rect_center_x, rect_center_y),
                radius=7,
                color=(0, 0, 255),
                thickness=-1,
            )

            direct_aurdino(
                rectangle_x=rect_center_x,
                rectangle_y=rect_center_y,
                center_height=center_height,
                center_width=center_width,
            )

        cv2.imshow("Faces", img)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cv2.destroyAllWindows()


def write(x):
    ARDUINO.write(bytes(str(x), "utf-8"))
    # time.sleep(0.05)


def direct_aurdino(rectangle_x, rectangle_y, center_height, center_width):
    if (
        int(rectangle_y) >= int(center_height) + OFFSET
        and int(rectangle_x) >= int(center_width) + OFFSET
    ):
        print("Too low and too far left")
        write("1")

    elif (
        int(rectangle_y) >= int(center_height) + OFFSET
        and int(rectangle_x) <= int(center_width) - OFFSET
    ):
        print("Too low and too far right")
        write("2")

    elif (
        int(rectangle_y) <= int(center_height) - OFFSET
        and int(rectangle_x) >= int(center_width) + OFFSET
    ):
        print("Too high and too far left")
        write("3")

    elif (
        int(rectangle_y) <= int(center_height) - OFFSET
        and int(rectangle_x) <= int(center_width) - OFFSET
    ):
        print("Too high and too far right")
        write("4")

    elif int(rectangle_y) >= int(center_height) + OFFSET:
        print("Too low")
        write("5")

    elif int(rectangle_y) <= int(center_height) - OFFSET:
        print("Too high")
        write("6")

    elif int(rectangle_x) >= int(center_width) + OFFSET:
        print("Too far left")
        write("7")

    elif int(rectangle_x) <= int(center_width) - OFFSET:
        print("Too far right")
        write("8")

    else:
        print("Centered")
        write("0")


if __name__ == "__main__":
    main()
