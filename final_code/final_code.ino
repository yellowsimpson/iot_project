#include <Servo.h>

#define SERVO_PIN     9
#define IR_SENSOR_PIN 8

Servo myServo;
bool sent = false;

void setup() {
  pinMode(IR_SENSOR_PIN, INPUT);
  myServo.attach(SERVO_PIN);
  myServo.write(0);
  Serial.begin(9600);
}

void loop() {
  int irState = digitalRead(IR_SENSOR_PIN);

  // IR 감지되었고 아직 라즈베리파이에 전송하지 않았을 때
  if (irState == LOW && !sent) {
    Serial.println("1");  // 라즈베리파이에게 알림
    sent = true;          // 중복 전송 방지
  } else if (irState == HIGH) {
    sent = false;         // 물체가 사라지면 다시 전송 가능하도록
  }

  // 라즈베리파이로부터 색상 문자열 수신
  if (Serial.available()) {
    String color = Serial.readStringUntil('\n');
    color.trim();

    if (color == "red") {
      Serial.println("빨강 감지 -> 서보 0도");
      myServo.write(0);
    } else if (color == "green") {
      Serial.println("초록 감지 -> 서보 45도");
      myServo.write(45);
    } else if (color == "blue") {
      Serial.println("파랑 감지 -> 서보 90도");
      myServo.write(90);
    } else if (color == "yellow") {
      Serial.println("노랑 감지 -> 서보 135도");
      myServo.write(135);
    }
  }

  delay(100);
}
