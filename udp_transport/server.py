import cv2
import socket
import struct
import pickle

# 소켓 설정
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 8485))  # 모든 IP로부터 연결 허용
server_socket.listen(1)

print("클라이언트를 기다리는 중...")
conn, addr = server_socket.accept()
print(f"{addr}에서 연결됨")

# 웹캠 시작
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 프레임 직렬화
    data = pickle.dumps(frame)
    message = struct.pack("Q", len(data)) + data  # 프레임 길이 + 데이터

    # 클라이언트로 전송
    try:
        conn.sendall(message)
    except:
        break

# 리소스 정리
cap.release()
conn.close()
server_socket.close()
