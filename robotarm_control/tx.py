import serial
import time

# 아두이노와 연결된 포트를 확인해서 아래에 입력하세요 (예: COM3, /dev/ttyUSB0 등)
arduino_port = '/dev/ttyUSB0'
baud_rate = 115200

# 시리얼 포트 열기
with serial.Serial(arduino_port, baud_rate, timeout=1) as ser:
    time.sleep(2)  # 아두이노 리셋 대기
    ser.write(b'a')  # 'a' 전송
    print("Sent 'a' to Arduino.")
