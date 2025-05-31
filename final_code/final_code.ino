#include <Servo.h>

#define SERVO_PIN     9
#define IR_SENSOR_PIN 8

Servo myServo;

void setup() {
  pinMode(IR_SENSOR_PIN, INPUT);
  myServo.attach(SERVO_PIN);
  myServo.write(0); // 초기 위치
  Serial.begin(9600);
}

void loop() {
  int irState = digitalRead(IR_SENSOR_PIN);

  if (irState == LOW) {
    Serial.println("1");     // '1' 전송
    myServo.write(90);
  } else {
    Serial.println("0");     // '0' 전송 (선택적)
    myServo.write(0);
  }

  delay(200);
}
