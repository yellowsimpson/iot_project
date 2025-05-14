#include <Servo.h>

// 서보 객체 선언
Servo base;
Servo shoulder;
Servo upperarm;
Servo middlearm;
Servo forearm;
Servo gripper;

// 초기 각도 설정 (모두 90도 = 중립 위치)
int baseAngle = 90;
int shoulderAngle = 90;
int upperarmAngle = 90;
int middlearmAngle = 90;
int forearmAngle = 90;
int gripperAngle = 90;

void setup() {
  Serial.begin(115200);

  // 서보 핀 연결 및 초기 각도 설정
  base.attach(3);
  base.write(baseAngle);

  shoulder.attach(5);
  shoulder.write(shoulderAngle);

  upperarm.attach(6);
  upperarm.write(upperarmAngle);

  middlearm.attach(7);
  middlearm.write(middlearmAngle);

  forearm.attach(8);
  forearm.write(forearmAngle);

  gripper.attach(9);
  gripper.write(gripperAngle);

}

void loop() {
  // 각 서보를 중립 위치로 이동 (원점 복원용)
  base.write(90);
  shoulder.write(90);
  upperarm.write(90);
  middlearm.write(90);
  forearm.write(90);
  gripper.write(90);

  delay(2000); // 2초 대기
}

