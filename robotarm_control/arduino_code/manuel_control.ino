#include <Servo.h>

Servo base, shoulder, upperarm, forearm, gripper;

int basepin = 3;
int shoulderpin = 4;
int upperarmpin = 6;
int forearmpin = 7;
int gripperpin = 8;

void setup() {
  Serial.begin(115200);
  base.attach(basepin);
  shoulder.attach(shoulderpin);
  upperarm.attach(upperarmpin);
  forearm.attach(forearmpin);
  gripper.attach(gripperpin);
}

void loop() {
  if (Serial.available()) {
    String inString = Serial.readStringUntil('\n');

    int baseVal = inString.substring(inString.indexOf('a') + 1, inString.indexOf('b')).toInt();
    int shoulderVal = inString.substring(inString.indexOf('b') + 1, inString.indexOf('c')).toInt();
    int upperarmVal = inString.substring(inString.indexOf('c') + 1, inString.indexOf('d')).toInt();
    int forearmVal = inString.substring(inString.indexOf('d') + 1, inString.indexOf('e')).toInt();
    int gripperVal = inString.substring(inString.indexOf('e') + 1, inString.indexOf('f')).toInt();

    base.write(baseVal);
    shoulder.write(shoulderVal);
    upperarm.write(upperarmVal);
    forearm.write(forearmVal);
    gripper.write(gripperVal);
  }
}
