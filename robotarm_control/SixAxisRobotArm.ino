//6-axis_robotarm_control.py 코드 실행시킬때 아두이노에 넣어야되는 코드

#include <Servo.h>

// 서보 객체 선언
Servo base;
Servo shoulder;
Servo upperarm;
Servo middlearm;
Servo forearm;
Servo gripper;

void setup() {
  Serial.begin(115200);

  // 서보 핀 연결
  base.attach(3);
  shoulder.attach(5);
  upperarm.attach(6);
  middlearm.attach(7);
  forearm.attach(8);
  gripper.attach(9);
}

void loop() {
  if (Serial.available()) {
    String command = Serial.readStringUntil('\n');  // 줄 끝까지 읽음

    int baseAngle = parseAngle(command, 'a');
    int shoulderAngle = parseAngle(command, 'b');
    int upperarmAngle = parseAngle(command, 'c');
    int middlearmAngle = parseAngle(command, 'd');
    int forearmAngle = parseAngle(command, 'e');
    int gripperAngle = parseAngle(command, 'f');

    // 각도 유효성 검사 및 적용
    if (baseAngle >= 0) base.write(baseAngle);
    if (shoulderAngle >= 0) shoulder.write(shoulderAngle);
    if (upperarmAngle >= 0) upperarm.write(upperarmAngle);
    if (middlearmAngle >= 0) middlearm.write(middlearmAngle);
    if (forearmAngle >= 0) forearm.write(forearmAngle);
    if (gripperAngle >= 0) gripper.write(gripperAngle);
  }
}

// 특정 문자(label) 뒤의 정수를 파싱하는 함수
int parseAngle(String data, char label) {
  int startIndex = data.indexOf(label);
  if (startIndex == -1) return -1;

  int endIndex = data.length();
  for (char nextLabel = label + 1; nextLabel <= 'f'; nextLabel++) {
    int tempIndex = data.indexOf(nextLabel, startIndex + 1);
    if (tempIndex != -1 && tempIndex < endIndex) {
      endIndex = tempIndex;
    }
  }

  String angleStr = data.substring(startIndex + 1, endIndex);
  return angleStr.toInt();  // 문자열을 정수로 변환
}
