#include <Servo.h>

Servo sorterServo;  // 분류 서보 (D8)
Servo doorServo;    // 문 서보 (D9)

String input = "";
bool rotationDone = false;
bool startReturn = false;
int sorterAngle = 0;

void setup() {
    Serial.begin(9600);
    sorterServo.attach(8);
    doorServo.attach(9);

    sorterServo.write(0);
    doorServo.write(0);
}

void loop() {
    if (Serial.available() > 0) {
        input = Serial.readStringUntil('\n');
        input.trim();

        // red 입력 들어오면 90도 천천히 회전
        if (input == "red") {
            for (int pos = 0; pos <= 90; pos++) {
                sorterServo.write(pos);
                delay(10);
            }
            sorterAngle = 90;

            delay(3000);         // 3초 대기
            rotationDone = true; // 회전 완료
        }

        // blue 입력 들어오면 회전 x
        else if (input == "blue") {
            sorterServo.write(0);
            sorterAngle = 0;

            doorServo.write(90);
            delay(1000);
            doorServo.write(0);
        }
    }

    // 분류 서보 회전이 끝나면 문 열림
    if (rotationDone) {
        doorServo.write(90);
        delay(1000);          // 문 열려 있는 시간 1초
        doorServo.write(0);

        // 문 다 닫힌 후에 복귀 시작 플래그 켜기
        startReturn = true;
        rotationDone = false;
    }

    // 분류 서보 원위치
    if (startReturn) {
        delay(300);
        for (int pos = 90; pos >= 0; pos--) {
            sorterServo.write(pos);
            delay(10);
        }
        sorterAngle = 0;
        startReturn = false;
    }
}
