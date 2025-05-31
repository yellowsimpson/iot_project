import serial
import time
import cv2
import numpy as np
from picamera2 import Picamera2

# 아두이노와 시리얼 연결
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
time.sleep(2)  # 시리얼 초기화 대기

# 색상 범위 정의 (HSV)
color_ranges = {
    'red': [
        ((0, 120, 70), (10, 255, 255)),   # 빨강 범위 1
        ((170, 120, 70), (180, 255, 255)) # 빨강 범위 2 (양쪽 끝)
    ],
    'green': [((40, 70, 70), (80, 255, 255))],
    'blue': [((100, 150, 70), (140, 255, 255))],
    'yellow': [((20, 100, 100), (30, 255, 255))]
}

def detect_color(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    for color, ranges in color_ranges.items():
        mask = np.zeros(hsv.shape[:2], dtype=np.uint8)
        for lower, upper in ranges:
            mask |= cv2.inRange(hsv, np.array(lower), np.array(upper))
        # 검출된 픽셀 수가 일정 이상이면 색상 감지로 간주
        if cv2.countNonZero(mask) > 500:
            return color
    return None

camera_on = False

while True:
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').strip()
        print(f"아두이노로부터 수신: {line}")
        
        if line == '1' and not camera_on:
            camera_on = True
            print("카메라 실행 중...")

            # 카메라 실행
            picam2 = Picamera2()
            preview_config = picam2.create_preview_configuration()
            picam2.configure(preview_config)
            picam2.start()

            detected = None
            start_time = time.time()

            while True:
                frame = picam2.capture_array()
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

                detected = detect_color(frame)
                if detected:
                    print(f"감지된 색상: {detected}")
                    ser.write((detected + "\n").encode())  # 아두이노에 전송
                    time.sleep(1)  # 중복 전송 방지
                    break

                # 카메라 화면 보기
                cv2.imshow("RPi Camera Live", frame)
                if cv2.waitKey(1) == ord('q') or time.time() - start_time > 15:
                    break  # 15초 후 자동 종료

            picam2.close()
            cv2.destroyAllWindows()
            camera_on = False
