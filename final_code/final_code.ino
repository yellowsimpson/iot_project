#include <Servo.h>

#define STEP_PIN 2
#define DIR_PIN 3
#define SERVO_PIN 9
#define IR_SENSOR_PIN 8

Servo servo_door;
bool sent = false;

// 색상별 목표 위치 (스텝 수 기준)
#define RED_POS     0
#define GREEN_POS   100
#define BLUE_POS    200
#define YELLOW_POS  300

int currentPos = 0;  // 현재 위치 기록

// 스텝핑 모터 회전 함수
void rotateStepper(int steps, bool clockwise) {
  digitalWrite(DIR_PIN, clockwise ? HIGH : LOW);
  for (int i = 0; i < steps; i++) {
    digitalWrite(STEP_PIN, HIGH);
    delayMicroseconds(800);  // 속도 조절
    digitalWrite(STEP_PIN, LOW);
    delayMicroseconds(800);
  }
}

// 지정된 위치로 이동하는 함수
void moveTo(int targetPos) {
  int diff = targetPos - currentPos;
  bool clockwise = diff >= 0;
  rotateStepper(abs(diff), clockwise);
  currentPos = targetPos;
}

void setup() {
  pinMode(IR_SENSOR_PIN, INPUT);
  pinMode(STEP_PIN, OUTPUT);
  pinMode(DIR_PIN, OUTPUT);
  servo_door.attach(SERVO_PIN);
  servo_door.write(0);
  Serial.begin(115200);
}

void loop() {
  int irState = digitalRead(IR_SENSOR_PIN);

  // IR 센서 감지 신호 전송 (1회만)
  if (irState == LOW && !sent) {
    Serial.println("1");  // 라즈베리파이에 신호 보냄
    sent = true;
  } else if (irState == HIGH) {
    sent = false;
  }

  // 색상 수신 처리
  if (Serial.available()) {
    String color = Serial.readStringUntil('\n');
    color.trim();

    if (color == "red") {
      Serial.println("빨강 감지 → 위치 0으로 이동");
      moveTo(RED_POS);
    } else if (color == "green") {
      Serial.println("초록 감지 → 위치 100으로 이동");
      moveTo(GREEN_POS);
    } else if (color == "blue") {
      Serial.println("파랑 감지 → 위치 200으로 이동");
      moveTo(BLUE_POS);
    } else if (color == "yellow") {
      Serial.println("노랑 감지 → 위치 300으로 이동");
      moveTo(YELLOW_POS);
    }

    // 스텝핑 모터 동작 후 서보 모터 제어
    delay(300);  // 모터 안정화
    servo_door.write(90);
    delay(500);
    servo_door.write(0);
    delay(500);
  }

  delay(100);
}
