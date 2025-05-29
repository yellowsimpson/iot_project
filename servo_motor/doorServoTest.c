#include <Servo.h>

Servo doorServo;   // 문 여는 서보 (D9)
String input = "";

void setup() {
    Serial.begin(9600);
    doorServo.attach(9);
    doorServo.write(0);  // 문 닫힌 상태로 시작
}

void loop() {
    if (Serial.available() > 0) {
        input = Serial.readStringUntil('\n');
        input.trim();

        if (input == "open") {
            doorServo.write(90);   // 문 열기
            delay(1000);           // 열려 있는 시간
            doorServo.write(0);    // 문 닫기
        }
    }
}
