#include <Servo.h>

Servo base, shoulder, upperarm, forearm, gripper;

void setup() {
  Serial.begin(115200);
  base.attach(4);
  shoulder.attach(5);
  upperarm.attach(6);
  forearm.attach(7);
  gripper.attach(8);
}

void loop() {
  if (Serial.available()) {
    String data = Serial.readStringUntil('\n'); // 한 줄씩 읽기

    int a = getValue(data, 'a', 'b');
    int b = getValue(data, 'b', 'c');
    int c = getValue(data, 'c', 'd');
    int d = getValue(data, 'd', 'e');
    int e = getValue(data, 'e', 'f');

    base.write(a);
    shoulder.write(b);
    upperarm.write(c);
    forearm.write(d);
    
    int gripperMapped = map(e, 0, 60, 90, 180); // 이 부분이 핵심
    gripper.write(gripperMapped);
  }
}

int getValue(String data, char startChar, char endChar) {
  int start = data.indexOf(startChar) + 1;
  int end = data.indexOf(endChar);
  if (start > 0 && end > start) {
    return data.substring(start, end).toInt();
  } else {
    return 90; // 기본값
  }
}
