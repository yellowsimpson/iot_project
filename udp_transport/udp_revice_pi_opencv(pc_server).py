# -*- coding:utf-8 -*-
import cv2
import numpy as np
import socket
import pickle
import struct

# UDP 설정
video_receive_port = 5005  # 라즈베리파이로부터 영상 데이터를 수신할 포트

# 영상 수신 소켓 생성 및 바인딩
video_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
video_sock.bind(("0.0.0.0", video_receive_port))

print("라즈베리파이로부터 영상 수신 대기 중...")

while True:
    try:
        # 영상 데이터 수신
        video_data, video_addr = video_sock.recvfrom(65507)
        video_size = struct.unpack("Q", video_data[:8])[0]
        video_frame_data = video_data[8:8 + video_size]

        # 영상 디코딩
        img = pickle.loads(video_frame_data)
        img = cv2.imdecode(img, cv2.IMREAD_COLOR)

        if img is None:
            print("프레임 디코딩 실패. 다음 프레임으로 넘어갑니다.")
            continue

        # 영상 출력
        cv2.imshow('Received Video', img)
        key = cv2.waitKey(1)
        if key & 0xff == ord('q'):
            break

    except Exception as e:
        print(f"영상 수신 중 오류: {e}")
        continue

# 종료 처리
cv2.destroyAllWindows()
video_sock.close()
print("프로그램 종료.")
