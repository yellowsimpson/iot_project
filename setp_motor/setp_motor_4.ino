#define STEP_PIN 2
#define DIR_PIN 3

#define STEPS_PER_REV 200
#define MICROSTEPS 1
#define STEP_DELAY 1000  // 느리게 해서 안정적인 회전

int currentPosition = 1;  // 시작은 1번 위치 (0도)

void setup() {
  pinMode(STEP_PIN, OUTPUT);
  pinMode(DIR_PIN, OUTPUT);
  Serial.begin(9600);
  Serial.println("위치 신호를 입력하세요 (1~4):");
}

void loop() {
  if (Serial.available() > 0) {
    int targetPosition = Serial.parseInt();

    if (targetPosition >= 1 && targetPosition <= 4) {
      rotateToPosition(targetPosition);
    }
  }
}

void rotateToPosition(int targetPosition) {
  int anglePerSection = 90;
  int angleToRotate = (targetPosition - currentPosition) * anglePerSection;

  // 음수면 반대 방향
  if (angleToRotate < 0) {
    digitalWrite(DIR_PIN, HIGH);  // 반시계방향
    angleToRotate = -angleToRotate;
  } else {
    digitalWrite(DIR_PIN, LOW);   // 시계방향
  }

  rotateStepper(angleToRotate);
  currentPosition = targetPosition;

  Serial.print("이동 완료 → 위치 ");
  Serial.println(currentPosition);
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
