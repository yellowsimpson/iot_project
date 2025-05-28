#define STEP_PIN 3
#define DIR_PIN 2

void setup() {
  pinMode(STEP_PIN, OUTPUT);
  pinMode(DIR_PIN, OUTPUT);

  digitalWrite(DIR_PIN, HIGH); // 시계방향
}

void loop() {
  digitalWrite(STEP_PIN, HIGH);
  delayMicroseconds(800);  // 속도 조절 (더 짧으면 빠름)
  digitalWrite(STEP_PIN, LOW);
  delayMicroseconds(800);
}
