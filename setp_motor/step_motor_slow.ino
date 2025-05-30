#define STEP_PIN 3
#define DIR_PIN 2

// 모터/드라이버 설정
#define STEPS_PER_REV 200   // 360도 = 200 스텝 (1.8도/step)
#define MICROSTEPS 1        // 마이크로스텝 비율 (1/1 풀스텝 기준)
#define STEP_DELAY 800      // 마이크로초 지연 시간

void setup() {
  pinMode(STEP_PIN, OUTPUT);
  pinMode(DIR_PIN, OUTPUT);

  // 시계방향 회전
  digitalWrite(DIR_PIN, HIGH);

  // 360도를 4등분: 각 90도씩 회전 → 멈춤
  for (int i = 0; i < 4; i++) {
    rotateStepper(90);      // 90도 회전
    delay(1000);            // 1초 정지 (필요 시 시간 조절)
  }

  // 작업 끝나면 loop 멈춤
  while (true);
}

void loop() {
  // 빈 루프
}

void rotateStepper(int angle) {
  int stepsToMove = angle * STEPS_PER_REV * MICROSTEPS / 360;

  for (int i = 0; i < stepsToMove; i++) {
    digitalWrite(STEP_PIN, HIGH);
    delayMicroseconds(STEP_DELAY);
    digitalWrite(STEP_PIN, LOW);
    delayMicroseconds(STEP_DELAY);
  }
}
