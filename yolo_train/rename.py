import os

folder = r"C:\Users\shims\Desktop\data_set\green_box"  # 파일들이 있는 폴더 경로
prefix = 'green_'  # 붙이고 싶은 접두사

for filename in os.listdir(folder):
    old_path = os.path.join(folder, filename)
    if os.path.isfile(old_path):
        new_filename = prefix + filename
        new_path = os.path.join(folder, new_filename)
        os.rename(old_path, new_path)

print("파일 이름이 변경되었습니다.")

