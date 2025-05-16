#include <Servo.h>

Servo myServo;
int servoPin = 9;

void setup() {
  Serial.begin(115200);        // 시리얼 통신 시작 (PC와 통신)
  myServo.attach(servoPin);  // 서보모터 연결
}

void loop() {
  if (Serial.available() > 0) {
    char received = Serial.read();  // 수신된 데이터 읽기

    if (received == 'a') {
      myServo.write(0);
      delay(1000);
      myServo.write(90);
      delay(1000);
      myServo.write(180);
      delay(1000);
    }
  }
}
