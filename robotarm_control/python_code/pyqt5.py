import sys
import serial
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QSlider, QLabel, QHBoxLayout
from PyQt5.QtCore import Qt

# 아두이노 시리얼 포트 설정 (포트 이름은 환경에 맞게 수정하세요)
ser = serial.Serial('/dev/ttyACM0', 115200)  # Windows: COMx, Linux/Mac: '/dev/ttyUSB0'

class ServoControlApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("로봇암 서보 제어기")
        self.setGeometry(100, 100, 400, 300)

        self.sliders = []
        self.labels = ['Base', 'Shoulder', 'UpperArm', 'ForeArm', 'Gripper']
        self.values = [90, 90, 90, 90, 0]  # 초기값 설정

        layout = QVBoxLayout()

        for i, name in enumerate(self.labels):
            h_layout = QHBoxLayout()
            label = QLabel(f"{name}: ")
            slider = QSlider(Qt.Horizontal)
            slider.setMinimum(0)
            slider.setMaximum(180 if name != 'Gripper' else 60)
            slider.setValue(self.values[i])
            slider.valueChanged.connect(self.send_servo_data)
            self.sliders.append(slider)
            h_layout.addWidget(label)
            h_layout.addWidget(slider)
            layout.addLayout(h_layout)

        self.setLayout(layout)
        self.send_servo_data()  # 초기값 전송

    def send_servo_data(self):
        values = [slider.value() for slider in self.sliders]
        command = f"a{values[0]}b{values[1]}c{values[2]}d{values[3]}e{values[4]}f\n"
        print(f"Sending: {command.strip()}")
        ser.write(command.encode())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ServoControlApp()
    window.show()
    sys.exit(app.exec_())
