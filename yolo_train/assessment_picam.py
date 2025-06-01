from picamera2 import Picamera2
import cv2
from ultralytics import YOLO

# YOLO ?? ??
model = YOLO('/home/pi/github/iot_project/yolo_train/train/weights/best.pt')

# Picamera2 ???
picam2 = Picamera2()
preview_config = picam2.create_preview_configuration()
picam2.configure(preview_config)
picam2.start()

# ??? ?? ??
while True:
    # ??? ??? ?? (RGB)
    frame = picam2.capture_array()
    
    # YOLO ??? BGR ???? ????? RGB ? BGR ??
    frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    # YOLO ??
    results = model(frame_bgr)

    # ?? ???
    plotted_frame = results[0].plot()

    # ??? ??
    cv2.imshow("YOLO + PiCamera", plotted_frame)

    # 'q' ?? ??? ??
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# ?? ??
cv2.destroyAllWindows()
picam2.close()