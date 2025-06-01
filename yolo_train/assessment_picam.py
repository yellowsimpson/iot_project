from picamera2 import Picamera2
import cv2
from ultralytics import YOLO

# YOLO 모델 로드
model = YOLO('/home/pi/github/iot_project/yolo_train/train/weights/best.pt')

# Picamera2 초기화
picam2 = Picamera2()
preview_config = picam2.create_preview_configuration()
picam2.configure(preview_config)
picam2.start()

# 실시간 처리 루프
while True:
    # 카메라 프레임 캡처 (RGB)
    frame = picam2.capture_array()
    
    # YOLO 모델은 BGR 이미지를 기대하므로 RGB → BGR 변환
    frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    # YOLO 추론
    results = model(frame_bgr)

    # 결과 시각화
    plotted_frame = results[0].plot()

    # 화면에 표시
    cv2.imshow("YOLO + PiCamera", plotted_frame)

    # 'q' 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 종료 처리
cv2.destroyAllWindows()
picam2.close()
