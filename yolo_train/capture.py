from picamera2 import Picamera2
import cv2
import time
import os

# 저장 폴더 설정
save_dir = "/home/pi/github/iot_project/data_set"
os.makedirs(save_dir, exist_ok=True)

# 카메라 초기화
picam2 = Picamera2()
preview_config = picam2.create_preview_configuration()
picam2.configure(preview_config)
picam2.start()

count = 1

try:
    while True:
        # 프레임 캡처
        frame = picam2.capture_array()
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        # 이미지 저장
        filename = os.path.join(save_dir, f"image_{count}.jpg")
        cv2.imwrite(filename, frame)
        print(f"{filename} 저장됨.")

        count += 1
        time.sleep(1)  # 1초 대기

except KeyboardInterrupt:
    print("촬영 중단됨.")

finally:
    picam2.close()
