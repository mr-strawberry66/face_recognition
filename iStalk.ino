#include <Servo.h>

Servo servoX;
Servo servoY;

int a, b, X;
int XAxis = 0;
int YAxis = 1;

void setup() {
    // Set the Serial monitor baude rate and launching
    Serial.begin(115200);
    Serial.setTimeout(1);

    // Declare the pin modes and servo pins
    pinMode(XAxis, INPUT);
    servoX.attach(8);
    pinMode(YAxis, INPUT);
    servoY.attach(9);
}

void loop() {
    while (!Serial.available());
    // Read servo positions
    a = servoX.read();
    b = servoY.read();

    X = Serial.readString().toInt();

    if (X == 1 || X == 2 || X == 5) {
        b = b + 1;
        servoY.write(b);
        // Too low
    }

    if (X == 3 || X == 4 || X == 6) {
        b = b - 1;
        servoY.write(b);
        // Too high
    }

    if (X == 1 || X == 3 || X == 7) {
        a = a - 1;
        servoX.write(a);
        // Too far left
    }

    if (X == 2 || X == 4 || X == 8) {
        a = a + 1;
        servoX.write(a);
        // Too far right
    }
}
