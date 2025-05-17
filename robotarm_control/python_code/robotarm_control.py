'''
MIT License

...

'''
import serial
import tkinter as tk
from tkinter import ttk
from math import sin, cos, pi
import time

# 시리얼 통신 설정
ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)  # COM 포트 및 보레이트 설정

# GUI 설정
root = tk.Tk()
root.title("Robot Arm Control")

# 윈도우 크기 조절
root.geometry("800x600")

# 캔버스 생성
canvas = tk 

a.Canvas(root)
canvas.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=20, pady=20)  # 여백 설정

# 프레임 생성
frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=frame, anchor='nw')  # 캔버스에 프레임 추가

# 각도 설정 함수
def set_angles():
    base_angle = base_scale.get()  # Base 각도를 스케일에서 가져옴
    shoulder_angle = shoulder_scale.get()  # Shoulder 각도를 스케일에서 가져옴
    upperarm_angle = upperarm_scale.get()  # Upperarm 각도를 스케일에서 가져옴
    forearm_angle = forearm_scale.get()  # Forearm 각도를 스케일에서 가져옴
    # 각도 값을 시리얼 통신을 통해 Arduino로 전송
    angles = "2a" + str(base_angle) + "b" + str(shoulder_angle) + "c" + str(upperarm_angle) + "d" + str(forearm_angle) + "e\n"
    ser.write(angles.encode())  # 문자열을 바이트로 변환하여 시리얼 통신으로 전송

# 동작 기록 리스트
recorded_actions = []

# 동작 기록 함수
def record_action():
    base_angle = base_scale.get()  # Base 각도를 스케일에서 가져옴
    shoulder_angle = shoulder_scale.get()  # Shoulder 각도를 스케일에서 가져옴
    upperarm_angle = upperarm_scale.get()  # Upperarm 각도를 스케일에서 가져옴
    forearm_angle = forearm_scale.get()  # Forearm 각도를 스케일에서 가져옴
    recorded_actions.append((base_angle, shoulder_angle, upperarm_angle, forearm_angle))
    update_action_list()  # 동작 기록이 추가될 때마다 리스트 업데이트

# 동작 실행 함수
def execute_actions():
    for action in recorded_actions:
        base_angle, shoulder_angle, upperarm_angle, forearm_angle = action
        angles = "2a" + str(base_angle) + "b" + str(shoulder_angle) + "c" + str(upperarm_angle) + "d" + str(forearm_angle) + "e\n"
        ser.write(angles.encode())
        time.sleep(3)

# 동작 리스트 업데이트 함수
def update_action_list():
    action_listbox.delete(0, tk.END)
    for i, action in enumerate(recorded_actions):
        action_listbox.insert(tk.END, f"Action {i+1}")

# 선택된 동작 표시 함수
def show_selected_action(evt):
    selected_index = action_listbox.curselection()
    if selected_index:
        selected_index = int(selected_index[0])
        base_angle, shoulder_angle, upperarm_angle, forearm_angle = recorded_actions[selected_index]
        selected_action_label.config(text=f"Base: {base_angle}, Shoulder: {shoulder_angle}, Upperarm: {upperarm_angle}, Forearm: {forearm_angle}")

# GUI 구성 요소 생성
base_label = tk.Label(frame, text="Base Angle:")  # Base 각도 입력 레이블
base_label.grid(row=0, column=0)  # 그리드 배치

base_scale = ttk.Scale(frame, from_=0, to=180, orient=tk.HORIZONTAL, length=300)  # Base 각도 입력 스케일
base_scale.grid(row=0, column=1)  # 그리드 배치

shoulder_label = tk.Label(frame, text="Shoulder Angle:")  # Shoulder 각도 입력 레이블
shoulder_label.grid(row=1, column=0)  # 그리드 배치

shoulder_scale = ttk.Scale(frame, from_=0, to=180, orient=tk.HORIZONTAL, length=300)  # Shoulder 각도 입력 스케일
shoulder_scale.grid(row=1, column=1)  # 그리드 배치

upperarm_label = tk.Label(frame, text="Upperarm Angle:")  # Upperarm 각도 입력 레이블
upperarm_label.grid(row=2, column=0)  # 그리드 배치

upperarm_scale = ttk.Scale(frame, from_=0, to=180, orient=tk.HORIZONTAL, length=300)  # Upperarm 각도 입력 스케일
upperarm_scale.grid(row=2, column=1)  # 그리드 배치

forearm_label = tk.Label(frame, text="Forearm Angle:")  # Forearm 각도 입력 레이블
forearm_label.grid(row=3, column=0)  # 그리드 배치

forearm_scale = ttk.Scale(frame, from_=0, to=180, orient=tk.HORIZONTAL, length=300)  # Forearm 각도 입력 스케일
forearm_scale.grid(row=3, column=1)  # 그리드 배치

set_button = tk.Button(frame, text="Set Angles", command=set_angles)  # 각도 설정 버튼
set_button.grid(row=4, columnspan=2)  # 그리드 배치

record_button = tk.Button(frame, text="Record Action", command=record_action)  # 동작 기록 버튼
record_button.grid(row=5, columnspan=2)  # 그리드 배치

execute_button = tk.Button(frame, text="Execute Actions", command=execute_actions)  # 동작 실행 버튼
execute_button.grid(row=6, columnspan=2)  # 그리드 배치

# 동작 리스트박스 생성
action_listbox = tk.Listbox(frame)
action_listbox.grid(row=7, columnspan=2, padx=5, pady=5)
action_listbox.bind('<<ListboxSelect>>', show_selected_action)

# 선택된 동작을 표시할 레이블
selected_action_label = tk.Label(frame, text="")
selected_action_label.grid(row=8, columnspan=2)

# 스크롤바 설정
vscrollbar = tk.Scrollbar(root, orient=tk.VERTICAL, command=canvas.yview)
vscrollbar.pack(side=tk.RIGHT, fill=tk.Y)
canvas.configure(yscrollcommand=vscrollbar.set)

hscrollbar = tk.Scrollbar(root, orient=tk.HORIZONTAL, command=canvas.xview)
hscrollbar.pack(side=tk.BOTTOM, fill=tk.X)
canvas.configure(xscrollcommand=hscrollbar.set)

canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))

# 원형 조이스틱 생성
joystick = tk.Canvas(frame, width=150, height=150, bg='white')
joystick.grid(row=9, columnspan=2, pady=10)
joystick.create_oval(10, 10, 140, 140, outline="black", width=2)
joystick_handle = joystick.create_oval(65, 65, 85, 85, fill="red")

def move_joystick(event):
    joystick.coords(joystick_handle, event.x-10, event.y-10, event.x+10, event.y+10)
    # Calculate angles based on joystick position
    x = event.x - 75
    y = event.y - 75
    base_angle = (x / 65) * 90 + 90  # Map x to 0-180 degrees
    shoulder_angle = (y / 65) * 90 + 90  # Map y to 0-180 degrees
    base_scale.set(base_angle)
    shoulder_scale.set(shoulder_angle)
    set_angles()

joystick.bind("<B1-Motion>", move_joystick)

root.mainloop()  # GUI 루프 실행