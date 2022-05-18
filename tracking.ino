#include <Servo.h>
#include <string.h>

Servo servo_x;
Servo servo_y;

int MOVEMENT_AMOUNT = 1;
int x_position, y_position;

std::string directions;


void setup() {
    // Set the Serial monitor baude rate
    Serial.begin(115200);
    Serial.setTimeout(1);

    // Declare the pin modes and servo pins
    pinMode(0, INPUT);
    servo_x.attach(8);
    pinMode(1, INPUT);
    servo_y.attach(9);
}


void loop() {
    while (!Serial.available());
    // Read servo positions
    x_position = servo_x.read();
    y_position = servo_y.read();

    directions = Serial.readString();

    for (char item : directions) {
        if (item == 'U') {
            y_position += MOVEMENT_AMOUNT;
            servo_y.write(y_position);
        }
        if (item == 'D') {
            y_position -= MOVEMENT_AMOUNT;
            servo_y.write(y_position);
        }
        if (item == 'L') {
            x_position -= MOVEMENT_AMOUNT;
            servo_x.write(x_position);
        }
        if (item == 'R') {
            x_position += MOVEMENT_AMOUNT;
            servo_x.write(x_position);
        }
    }
}
