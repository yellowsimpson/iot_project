#include <Servo.h>

// 서보 객체 선언
Servo base;
Servo shoulder;
Servo upperarm;
Servo forearm;
Servo gripper;

// 핀 번호 설정
int basepin = 3;
int shoulderpin = 5;
int upperarmpin = 6;
int forearmpin = 7;
int gripperpin = 8;

// 기준 각도
int defaultAngle = 90;
int moveRange = 60;
int gripperDefault = 0;
int gripperRange = 60;

// 서보를 부드럽게 움직이는 함수 (기본값과 범위 입력)
void testServo(Servo servo, int startAngle, int range) {
  for (int pos = startAngle; pos <= startAngle + range; pos++) {
    servo.write(pos);
    delay(15);
  }
  delay(500); // 끝점 대기

  for (int pos = startAngle + range; pos >= startAngle; pos--) {
    servo.write(pos);
    delay(15);
  }
  delay(1000); // 다음 서보 이동 전 대기
}

void setup() {
  base.attach(basepin);
  shoulder.attach(shoulderpin);
  upperarm.attach(upperarmpin);
  forearm.attach(forearmpin);
  gripper.attach(gripperpin);

  // 초기 위치 설정
  base.write(defaultAngle);
  shoulder.write(defaultAngle);
  upperarm.write(defaultAngle);
  forearm.write(defaultAngle);
  gripper.write(gripperDefault);
  delay(1000); // 초기 위치 정착 대기
}

void loop() {
  testServo(base, defaultAngle, moveRange);        // 90 → 150 → 90
  testServo(shoulder, defaultAngle, moveRange);
  testServo(upperarm, defaultAngle, moveRange);
  testServo(forearm, defaultAngle, moveRange);
  testServo(gripper, gripperDefault, gripperRange); // 0 → 60 → 0
}
