import cv2

def init_camera():
    cap = cv2.VideoCapture(2)  # 웹캠 인덱스 (필요시 0, 1로 변경)
    if cap.isOpened():
        print("카메라 초기화 성공.")
        return cap
    else:
        print("카메라 초기화 실패.")
        return None

def release_camera(cap):
    if cap is not None:
        cap.release()
        cv2.destroyAllWindows()
        print("카메라가 닫혔습니다.")

def main():
    cap = init_camera()
    if cap is None:
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("프레임을 읽을 수 없습니다.")
            break

        cv2.imshow("Camera Feed", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    release_camera(cap)

if __name__ == "__main__":
    main()
