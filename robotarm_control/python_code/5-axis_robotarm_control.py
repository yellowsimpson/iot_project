import serial
import tkinter as tk
from tkinter import ttk
import time

# 시리얼 통신 설정
try:
    ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
except serial.SerialException:
    print("Serial port not found. Please check the port.")
    ser = None

# GUI 설정
root = tk.Tk()
root.title("Robot Arm Control")
root.geometry("800x700")

# 프레임 생성
frame = tk.Frame(root)
frame.pack(padx=20, pady=20)

# 각도 설정 함수
def set_angles():
    if not ser:
        return
    base_angle = base_scale.get()
    shoulder_angle = shoulder_scale.get()
    upperarm_angle = upperarm_scale.get()
    forearm_angle = forearm_scale.get()
    gripper_angle = gripper_scale.get()
    angles = (
        f"2a{int(base_angle)}b{int(shoulder_angle)}c{int(upperarm_angle)}"
        f"d{int(forearm_angle)}e{int(gripper_angle)}f\n"
    )
    ser.write(angles.encode())

# 동작 기록 리스트
recorded_actions = []

def record_action():
    action = (
        base_scale.get(), shoulder_scale.get(), upperarm_scale.get(),
        forearm_scale.get(), gripper_scale.get()
    )
    recorded_actions.append(action)
    update_action_list()

def execute_actions():
    if not ser:
        return
    for action in recorded_actions:
        base_angle, shoulder_angle, upperarm_angle, forearm_angle, gripper_angle = action
        angles = (
            f"2a{int(base_angle)}b{int(shoulder_angle)}c{int(upperarm_angle)}"
            f"d{int(forearm_angle)}e{int(gripper_angle)}f\n"
        )
        ser.write(angles.encode())
        time.sleep(3)

# 초기 위치로 복귀 함수
def reset_position():
    base_scale.set(90)
    shoulder_scale.set(90)
    upperarm_scale.set(90)
    forearm_scale.set(90)
    gripper_scale.set(90)
    set_angles()

# 그리퍼 열기/닫기 상태
gripper_open = [False]

def toggle_gripper():
    if gripper_open[0]:
        gripper_scale.set(30)  # 닫기
    else:
        gripper_scale.set(120)  # 열기
    gripper_open[0] = not gripper_open[0]
    set_angles()

def update_action_list():
    action_listbox.delete(0, tk.END)
    for i, _ in enumerate(recorded_actions):
        action_listbox.insert(tk.END, f"Action {i+1}")

def show_selected_action(evt):
    selected_index = action_listbox.curselection()
    if selected_index:
        idx = int(selected_index[0])
        base, sh, up, fore, grip = recorded_actions[idx]
        selected_action_label.config(text=f"B:{base}, S:{sh}, U:{up}, F:{fore}, G:{grip}")

# 슬라이더 및 레이블 생성 함수
def create_servo_control(label_text, row):
    label = tk.Label(frame, text=label_text)
    label.grid(row=row, column=0)
    scale = ttk.Scale(frame, from_=0, to=180, orient=tk.HORIZONTAL, length=300)
    scale.grid(row=row, column=1)
    return scale

# 각 서보 컨트롤 생성
base_scale = create_servo_control("Base", 0)
shoulder_scale = create_servo_control("Shoulder", 1)
upperarm_scale = create_servo_control("Upperarm", 2)
forearm_scale = create_servo_control("Forearm", 3)
gripper_scale = create_servo_control("Gripper", 4)

# 버튼들
tk.Button(frame, text="Set Angles", command=set_angles).grid(row=6, columnspan=2, pady=5)
tk.Button(frame, text="Record Action", command=record_action).grid(row=7, columnspan=2, pady=5)
tk.Button(frame, text="Execute Actions", command=execute_actions).grid(row=8, columnspan=2, pady=5)
tk.Button(frame, text="Reset Position", command=reset_position).grid(row=9, columnspan=2, pady=5)
tk.Button(frame, text="Toggle Gripper", command=toggle_gripper).grid(row=10, columnspan=2, pady=5)

# 리스트 박스 및 선택 정보
action_listbox = tk.Listbox(frame)
action_listbox.grid(row=11, columnspan=2, pady=5)
action_listbox.bind('<<ListboxSelect>>', show_selected_action)

selected_action_label = tk.Label(frame, text="")
selected_action_label.grid(row=12, columnspan=2)

root.mainloop()
