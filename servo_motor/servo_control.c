#include <Servo.h> // 서보모터 라이브러리 포함

Servo myServo; // 서보 객체 생성

int servoPin = 9; // 서보모터 신호 핀 (PWM 핀 사용, 예: 9번)

void setup() {
  myServo.attach(servoPin); // 서보모터를 지정한 핀에 연결
}

void loop() {
  myServo.write(140);   // 90도 위치로 이동
  delay(1000);         // 1초 대기
  myServo.write(180);  // 180도 위치로 이동
  delay(1000);         // 1초 대기
}