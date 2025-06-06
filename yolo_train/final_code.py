import serial
import time
import cv2
from picamera2 import Picamera2
from ultralytics import YOLO

# 아두이노와 시리얼 통신 설정
ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
time.sleep(2)

# YOLOv8 모델 로드
model = YOLO('/home/pi/github/iot_project/yolo_train/train/weights/best.pt')
model.conf = 0.5  # 신뢰도 기준 설정

# 카메라 상태 플래그
camera_on = False

while True:
    # 아두이노로부터 IR 센서 신호 수신
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').strip()
        print(f"[수신] 아두이노로부터: {line}")

        if line == "1" and not camera_on:
            print("[시작] 블록 탐지 시작")
            camera_on = True

            # 카메라 설정
            picam2 = Picamera2()
            config = picam2.create_preview_configuration()
            picam2.configure(config)
            picam2.start()

            start_time = time.time()
            detected_color = None

            while True:
                # 카메라 프레임 캡처 (RGB)
                frame = picam2.capture_array()

                # YOLO 모델은 BGR 이미지를 기대하므로 RGB → BGR 변환
                frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

                # YOLOv8 객체 탐지 수행
                results = model(frame_bgr)[0]

                for result in results.boxes:
                    cls_id = int(result.cls[0])
                    conf = float(result.conf[0])
                    label = model.names[cls_id]

                    if label in ['red', 'blue', 'green', 'yellow']:
                        print(f"[감지] 색상 블록: {label}")

                        # 아두이노에 전송
                        ser.write((label + "\n").encode())
                        detected_color = label

                        # 바운딩 박스 그리기
                        x1, y1, x2, y2 = map(int, result.xyxy[0])
                        cv2.rectangle(frame_bgr, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        cv2.putText(frame_bgr, label, (x1, y1 - 10),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                        cv2.imshow("YOLOv8 Detection", frame_bgr)
                        cv2.waitKey(1000)
                        break

                if detected_color:
                    break

                # 탐지 안내 텍스트
                cv2.putText(frame_bgr, "Detecting block...", (30, 40),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                cv2.imshow("YOLOv8 Detection", frame_bgr)

                if cv2.waitKey(1) == ord('q') or (time.time() - start_time) > 15:
                    print("[종료] 감지 시간 초과")
                    break

            picam2.close()
            cv2.destroyAllWindows()
            camera_on = False
