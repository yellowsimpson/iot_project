import cv2
from ultralytics import YOLO

# model = YOLO('yolov8s.pt')
model = YOLO('C:\\Users\\shims\\Desktop\\github\\yolo_dectect_traing\\runs\\detect\\train2\\weights\\best.pt')
results = model('C:\\Users\\shims\\Desktop\\github\\yolo_dectect_traing\\box_data_1\\test\\images\\photo_195.jpg')

plots = results[0].plot()
cv2.imshow("plot", plots)
cv2.waitKey(0)
cv2.destroyAllWindows()
