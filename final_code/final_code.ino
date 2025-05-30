#include <Servo.h>

Servo base, shoulder, upperarm, forearm, gripper;
const int irPin = 2;

void setup() {
  Serial.begin(115200);
  base.attach(3);
  shoulder.attach(4);
  upperarm.attach(6);
  forearm.attach(7);
  gripper.attach(9);
  pinMode(irPin, INPUT);
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
    
    int gripperMapped = map(e, 0, 60, 90, 180);
    gripper.write(gripperMapped);
  }

  // IR 센서 상태 읽고 전송
  int irState = digitalRead(irPin);
  Serial.print("ir:");
  Serial.println(irState);
  delay(100);  // 100ms 주기로 전송
}

int getValue(String data, char startChar, char endChar) {
  int start = data.indexOf(startChar) + 1;
  int end = data.indexOf(endChar);
  if (start > 0 && end > start) {
    return data.substring(start, end).toInt();
  } else {
    return 90;
  }
}
