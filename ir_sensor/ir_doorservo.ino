#include <Servo.h>

#define SERVO_PIN 10       // 서보모터 제어 핀
#define IR_SENSOR_PIN 9   // IR 센서 디지털 출력 핀

Servo myServo;

void setup() {
  pinMode(IR_SENSOR_PIN, INPUT);
  myServo.attach(SERVO_PIN);
  myServo.write(0); // 초기 위치
  Serial.begin(9600);
}

void loop() {
  int irState = digitalRead(IR_SENSOR_PIN); // IR 센서 값 읽기 (0: 감지됨, 1: 없음)

  if (irState == LOW) {  // 물체 감지됨
    Serial.println("물체 감지됨!");
    myServo.write(90);   // 서보를 90도로 회전
  } else {
    Serial.println("감지 없음");
    myServo.write(0);    // 서보를 원래 위치로
  }

  delay(200); // 너무 자주 체크하지 않도록 약간의 지연
}
