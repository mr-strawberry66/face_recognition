import cv2
import os

OFFSET = 50
CASCADE_PATH = os.path.join("resources", "haarcascade_frontalface_default.xml")
CASCADE = cv2.CascadeClassifier(CASCADE_PATH)

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

        if int(rect_center_y) >= int(center_height) + OFFSET:
            print("Too low")

        elif int(rect_center_y) <= int(center_height) - OFFSET:
            print("Too high")

        else:
            print("Height centered")

        if int(rect_center_x) >= int(center_width) + OFFSET:
            print("Too far left")

        if int(rect_center_x) <= int(center_width) - OFFSET:
            print("Too far right")

        else:
            print("Width centered")

    cv2.imshow("Faces", img)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cv2.destroyAllWindows()
