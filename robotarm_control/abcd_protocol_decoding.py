import serial
import time

ser = serial.Serial('/dev/tty/ACM0', 115200)  # 포트 이름과 보레이트 확인
time.sleep(2)  # 아두이노 연결 안정화 대기

# 로봇암 명령 전송 (예: a90b100c120d110e95f)
command = "a90b100c120d110e95f\n"
ser.write(command.encode())
