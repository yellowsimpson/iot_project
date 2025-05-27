from picamera2 import Picamera2
import cv2

# 카메라 초기화
picam2 = Picamera2()
preview_config = picam2.create_preview_configuration()
picam2.configure(preview_config)

picam2.start()

while True:
    frame = picam2.capture_array()
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    cv2.imshow("RPi Camera Live", frame)

    if cv2.waitKey(1) == ord('q'):
        break

cv2.destroyAllWindows()
picam2.close()
