#include <Servo.h>

// 서보 객체 선언
Servo base;
Servo shoulder;
Servo upperarm;
Servo forearm;
Servo gripper;

// 초기 각도 설정 (모두 90도 = 중립 위치)
int baseAngle = 90;
int shoulderAngle = 95;
int upperarmAngle = 100;
int forearmAngle = 90;
int gripperAngle = 90;

void setup() {
  Serial.begin(115200);

  // 서보 핀 연결 및 초기 각도 설정
  base.attach(3);
  base.write(baseAngle);

  shoulder.attach(4);
  shoulder.write(shoulderAngle);

  upperarm.attach(6);
  upperarm.write(upperarmAngle);

  forearm.attach(7);
  forearm.write(forearmAngle);

  gripper.attach(9);
  gripper.write(gripperAngle);

}

void loop() {
  // 각 서보를 중립 위치로 이동 (원점 복원용)
  base.write(90);
  shoulder.write(95);
  upperarm.write(100);
  forearm.write(90);
  gripper.write(90);
  delay(2000); // 2초 대기
}

