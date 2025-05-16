import cv2
import socket
import struct
import pickle
import time

# UDP 설정
pc_ip = "172.30.1.42"           # 수신자 PC의 IP 주소
video_send_port = 5005          # 영상 데이터를 송신할 포트

# 영상 송신을 위한 소켓 생성
video_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 카메라 설정
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

# 카메라 확인
if not cap.isOpened():
    print("카메라를 열 수 없습니다.")
    exit(1)

print(f"카메라 영상 송신 중... (Ctrl + C로 종료)")

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("프레임을 읽을 수 없습니다.")
            break

        # JPEG 인코딩
        ret, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 50])
        if not ret:
            print("프레임 인코딩 실패")
            continue

        # 직렬화 후 송신
        try:
            data = pickle.dumps(buffer)
            video_sock.sendto(struct.pack("Q", len(data)) + data, (pc_ip, video_send_port))
            print("프레임 전송 완료")
        except Exception as e:
            print(f"영상 송신 중 오류: {e}")

        time.sleep(0.033)  # 30fps

except KeyboardInterrupt:
    print("사용자 종료 요청으로 프로그램을 종료합니다.")

finally:
    cap.release()
    video_sock.close()
    print("자원 정리 완료. 프로그램 종료.")
