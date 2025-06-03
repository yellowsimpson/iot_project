// A4988 드라이버로 스텝모터 제어하기 - 아두이노

const int dirPin = 2;    // 방향 제어 핀
const int stepPin = 3;   // 스텝 제어 핀
const int stepsPerRevolution = 200;  // 모터 한 바퀴당 스텝 수

void setup() {
  pinMode(stepPin, OUTPUT);
  pinMode(dirPin, OUTPUT);
}

void loop() {
  digitalWrite(dirPin, HIGH); // 시계 방향 회전
  for(int x = 0; x < stepsPerRevolution; x++) {
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(2000);
    digitalWrite(stepPin, LOW);
    delayMicroseconds(2000);
  }
  delay(1000); // 1초 대기

  digitalWrite(dirPin, LOW); // 시계 방향 회전
  for(int x = 0; x < stepsPerRevolution; x++) {
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(1000);
    digitalWrite(stepPin, LOW);
    delayMicroseconds(1000);
  }
  delay(1000); // 1초 대기

  digitalWrite(dirPin, HIGH); // 반시계 방향 회전
  for(int x = 0; x < 5 * stepsPerRevolution; x++) {
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(500);
    digitalWrite(stepPin, LOW);
    delayMicroseconds(500);
  }
  delay(1000); // 1초 대기
  digitalWrite(dirPin, LOW);
  for(int x = 0; x < 5 * stepsPerRevolution; x++){
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(500);
    digitalWrite(stepPin, LOW);
    delayMicroseconds(500);
  }
  delay(1000);
}