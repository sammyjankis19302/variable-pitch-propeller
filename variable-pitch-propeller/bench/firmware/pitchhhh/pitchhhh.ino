#include <Servo.h>

Servo myServo;

void setup() {
  myServo.attach(9);     // Attach servo to pin 9
  int angle = 120;        // <<< CHANGE THIS ANGLE (0 to 180)
  myServo.write(angle);  // Move servo to desired angle
}

void loop() {
  // Nothing here, angle set once in setup()
}
