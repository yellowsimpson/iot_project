import serial
import time
from picamera2 import Picamera2
import cv2

# 시리얼 포트 설정 (포트 이름은 연결된 아두이노에 따라 다름)
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)  # 포트가 다를 경우 수정 필요
time.sleep(2)  # 시리얼 초기화 대기

camera_on = False

while True:
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').strip()
        print(f"아두이노로부터 수신: {line}")
        
        if line == '1' and not camera_on:
            camera_on = True
            print("물체 감지됨! 카메라 실행")

            # 카메라 실행
            picam2 = Picamera2()
            preview_config = picam2.create_preview_configuration()
            picam2.configure(preview_config)
            picam2.start()

            while True:
                frame = picam2.capture_array()
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                cv2.imshow("RPi Camera Live", frame)

                if cv2.waitKey(1) == ord('q'):
                    print("카메라 종료")
                    break

            cv2.destroyAllWindows()
            picam2.close()
            camera_on = False
