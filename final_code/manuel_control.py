import sys
import serial
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QSlider, QLabel, QPushButton
)
from PyQt5.QtCore import Qt, QTimer, QPoint
from PyQt5.QtGui import QPainter, QPen, QColor


# 아두이노 포트 설정
ser = serial.Serial('/dev/ttyACM0', 115200)

class Joystick(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(150, 150)
        self.center = QPoint(75, 75)
        self.handle_pos = QPoint(75, 75)
        self.pressed = False
        self.offset = QPoint(0, 0)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.black, 2))
        painter.drawEllipse(25, 25, 100, 100)
        painter.setBrush(QColor(100, 100, 255, 180))
        painter.drawEllipse(self.handle_pos, 15, 15)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.pressed = True
            self.update_position(event.pos())

    def mouseMoveEvent(self, event):
        if self.pressed:
            self.update_position(event.pos())

    def mouseReleaseEvent(self, event):
        self.pressed = False
        self.handle_pos = self.center
        self.offset = QPoint(0, 0)
        self.update()

    def update_position(self, pos):
        dx = pos.x() - self.center.x()
        dy = pos.y() - self.center.y()
        distance = min((dx ** 2 + dy ** 2) ** 0.5, 50)

        if distance != 0:
            dx = int(50 * dx / distance)
            dy = int(50 * dy / distance)

        self.offset = QPoint(dx, dy)
        self.handle_pos = self.center + self.offset
        self.update()

    def get_offset(self):
        return self.offset


class ServoControlApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("로봇암 조이스틱 제어")
        self.setGeometry(100, 100, 500, 400)

        self.servo_labels = ['Base', 'Shoulder', 'UpperArm', 'ForeArm', 'Gripper']
        self.servo_values = [90, 95, 100, 90, 90]
        self.sliders = []

        main_layout = QVBoxLayout()

        # 조이스틱 레이아웃
        joystick_layout = QHBoxLayout()
        self.joystick1 = Joystick()
        self.joystick2 = Joystick()
        joystick_layout.addWidget(QLabel("Base / Shoulder"))
        joystick_layout.addWidget(self.joystick1)
        joystick_layout.addWidget(QLabel("UpperArm / ForeArm"))
        joystick_layout.addWidget(self.joystick2)
        main_layout.addLayout(joystick_layout)

        # 슬라이더 레이아웃
        for i, name in enumerate(self.servo_labels):
            h_layout = QHBoxLayout()
            label = QLabel(f"{name}: ")
            slider = QSlider(Qt.Horizontal)
            slider.setMinimum(0)
            slider.setMaximum(180 if name != 'Gripper' else 60)
            slider.setValue(self.servo_values[i])
            slider.valueChanged.connect(self.send_servo_data)
            self.sliders.append(slider)
            h_layout.addWidget(label)
            h_layout.addWidget(slider)
            main_layout.addLayout(h_layout)

        # 그리퍼 버튼
        self.gripper_open = False
        self.gripper_button = QPushButton("Toggle Gripper")
        self.gripper_button.clicked.connect(self.toggle_gripper)
        main_layout.addWidget(self.gripper_button)

        # 초기화 버튼
        self.reset_button = QPushButton("Reset Position")
        self.reset_button.clicked.connect(self.reset_positions)
        main_layout.addWidget(self.reset_button)

        self.setLayout(main_layout)

        # 타이머로 주기적 조이스틱 상태 확인
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_from_joysticks)
        self.timer.start(100)

        self.send_servo_data()

    def reset_positions(self):
        # 기본 위치 설정
        default_positions = [90, 95, 100, 90, 90]
        for i, val in enumerate(default_positions):
            self.sliders[i].setValue(val)
        
        # 조이스틱 위치 초기화
        for js in [self.joystick1, self.joystick2]:
            js.handle_pos = js.center
            js.offset = QPoint(0, 0)
            js.update()

        # 그리퍼 상태도 초기화
        self.gripper_open = False
        self.send_servo_data()

    def toggle_gripper(self):
        self.gripper_open = not self.gripper_open
        self.sliders[4].setValue(60 if self.gripper_open else 0)
        self.send_servo_data()

    def update_from_joysticks(self):
        # 조이스틱 1 → base (0), shoulder (1)
        offset1 = self.joystick1.get_offset()
        delta_base = int(offset1.x() / 10)
        delta_shoulder = int(-offset1.y() / 10)

        # 조이스틱 2 → upperarm (2), forearm (3)
        offset2 = self.joystick2.get_offset()
        delta_upperarm = int(offset2.x() / 10)
        delta_forearm = int(-offset2.y() / 10)

        deltas = [delta_base, delta_shoulder, delta_upperarm, delta_forearm]

        for i in range(4):  # gripper 제외
            new_val = self.sliders[i].value() + deltas[i]
            new_val = max(0, min(self.sliders[i].maximum(), new_val))
            self.sliders[i].setValue(new_val)

        self.send_servo_data()

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
