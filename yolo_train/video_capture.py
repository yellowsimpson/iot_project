import cv2
import os

# 폴더 경로
folder_path = r"/home/pi/github/iot_project/data_set"

# 해당 폴더 안의 모든 파일 리스트 가져오기
all_files = os.listdir(folder_path)

# 동영상 파일을 캡쳐된 이미지를 저장할 폴더
output_folder = 'C:\\Users\\shims\\Desktop\\save_picture'
os.makedirs(output_folder, exist_ok=True)

# 각 동영상 파일에 대해 처리
for file_name in all_files:
    # 파일 경로 생성
    file_path = os.path.join(folder_path, file_name)
    
    # 파일이 동영상인지 확인 (여기서는 .avi로 필터링)
    if file_name.endswith(".AVI"):  # 필요에 따라 다른 확장자 추가 가능
        print(f"Processing video: {file_name}")
        
        # 비디오 캡처 객체 생성
        cap = cv2.VideoCapture(file_path)

        # 초당 프레임 수 (FPS)
        fps = int(cap.get(cv2.CAP_PROP_FPS))

        # 1초마다 캡쳐하기 위해 프레임 간격 설정
        frame_interval = fps

        frame_count = 0
        image_count = 0

        while cap.isOpened():
            ret, frame = cap.read()

            if not ret:
                break

            # 1초마다 이미지 캡쳐 (frame_interval만큼 프레임이 지나면 캡쳐)
            if frame_count % frame_interval == 0:
                image_path = os.path.join(output_folder, f'{file_name}_image_{image_count}.jpg')
                cv2.imwrite(image_path, frame)
                print(f"Image saved: {image_path}")
                image_count += 1

            frame_count += 1

        # 비디오 객체 해제
        cap.release()

cv2.destroyAllWindows()
