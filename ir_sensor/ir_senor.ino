int IR = 2;
int LED = 13;

void setup() {
    pinMode(IR, INPUT);
    pinMode(LED, OUTPUT);
    Serial.begin(115200);
}

void loop() {
    int IRsensor = digitalRead(IR);

    if (IRsensor == LOW) {          // 물체 감지됨
        digitalWrite(LED, HIGH);    // LED 켬
        Serial.println(1);          // 1 출력
    }
    else {                          // 물체 감지되지 않음
        digitalWrite(LED, LOW);     // LED 끔
        Serial.println(0);          // 0 출력
    }

    delay(200); // 너무 빠르게 출력되는 걸 방지
}
