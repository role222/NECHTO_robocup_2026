import numpy as np
import cv2
from picamera2 import Picamera2
import json
import os

CALIB_FILE = "./color_calibrate/calibration.json"

def compute_opposite_lab_color(l_min, l_max, a_min, a_max, b_min, b_max):
    """Вычисляет средний LAB из диапазона, затем противоположный оттенок (инверсия a и b относительно 128) и возвращает кортеж BGR."""
    L = int((l_min + l_max) / 2)
    A = int((a_min + a_max) / 2)
    B = int((b_min + b_max) / 2)
    # Противоположный оттенок: L тот же, a' = 255 - A + 1, b' = 255 - B + 1
    A_opp = 255 - A + 1
    B_opp = 255 - B + 1
    lab_opp = np.array([[[L, A_opp, B_opp]]], dtype=np.uint8)
    bgr_opp = cv2.cvtColor(lab_opp, cv2.COLOR_LAB2BGR)[0, 0]
    return tuple(int(c) for c in bgr_opp)

def load_calibration(filepath):
    """Загружает JSON-калибровку. Возвращает словарь с данными или пустой словарь при ошибке."""
    if not os.path.exists(filepath):
        print(f"Файл калибровки {filepath} не найден!")
        return {}
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
        return data
    except Exception as e:
        print(f"Ошибка чтения JSON: {e}")
        return {}

def get_color_params(calib_data, cam_name, color_name):
    """Извлекает из калибровочных данных параметры для конкретной камеры и цвета.
    Возвращает (min_array, max_array, circle_color_bgr)."""
    key = f"{cam_name}_{color_name}"
    if key not in calib_data:
        raise KeyError(f"В калибровке отсутствует ключ '{key}'")
    d = calib_data[key]
    L1, a1, b1 = d['L1'], d['a1'], d['b1']
    L2, a2, b2 = d['L2'], d['a2'], d['b2']
    min_arr = np.array([L1, a1, b1], dtype=np.uint8)
    max_arr = np.array([L2, a2, b2], dtype=np.uint8)
    circle_color = compute_opposite_lab_color(L1, L2, a1, a2, b1, b2)
    return min_arr, max_arr, circle_color

# Загрузка калибровки
calib_data = load_calibration(CALIB_FILE)
if not calib_data:
    print("Не удалось загрузить калибровку. Завершение работы.")
    exit(1)

# Извлечение параметров для всех цветов и камер
try:
    # Камера 0
    cam0_red_min, cam0_red_max, cam0_red_color = get_color_params(calib_data, "cam0", "red")
    cam0_yellow_min, cam0_yellow_max, cam0_yellow_color = get_color_params(calib_data, "cam0", "yellow")
    cam0_blue_min, cam0_blue_max, cam0_blue_color = get_color_params(calib_data, "cam0", "blue")

    # Камера 1
    cam1_red_min, cam1_red_max, cam1_red_color = get_color_params(calib_data, "cam1", "red")
    cam1_yellow_min, cam1_yellow_max, cam1_yellow_color = get_color_params(calib_data, "cam1", "yellow")
    cam1_blue_min, cam1_blue_max, cam1_blue_color = get_color_params(calib_data, "cam1", "blue")
except KeyError as e:
    print(e)
    print("Проверьте, что калибровка была выполнена для всех цветов и камер.")
    exit(1)

# Инициализация камер
cam0 = Picamera2(1)
cam1 = Picamera2(0)
config0 = cam0.create_video_configuration(main={"size": (1296, 972)})
config1 = cam1.create_video_configuration(main={"size": (1296, 972)})
cam0.configure(config0)
cam1.configure(config1)
cam0.start()
cam1.start()

print("Запуск отслеживания. Нажмите 'q' для выхода.")

while True:
    # Захват кадров
    frame0 = cv2.cvtColor(cv2.flip(cam0.capture_array(), -1), cv2.COLOR_RGB2BGR)
    frame1 = cv2.cvtColor(cv2.flip(cam1.capture_array(), -1), cv2.COLOR_RGB2BGR)

    # Конвертация в LAB
    lab0 = cv2.cvtColor(frame0, cv2.COLOR_BGR2LAB)
    lab1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2LAB)

    # Функция для обработки одного цвета на одном кадре
    def process_color(lab_img, frame_img, min_val, max_val, circle_color):
        HFOV_DEG = 180.0
        mask = cv2.inRange(lab_img, min_val, max_val)
        moments = cv2.moments(mask, True)
        area = moments['m00']
        if area <= 100:
            return None
        x = int(moments['m10'] / area)
        y = int(moments['m01'] / area)
        cv2.circle(frame_img, (x, y), 10, circle_color, -1)
        h, w = lab_img.shape[:2]
        center_x = w / 2.0
        dx_norm = (x - center_x) / (w / 2.0)
        angle = dx_norm * (HFOV_DEG / 2.0)
        return angle

    # Камера 0
    ball_angle_0 = process_color(lab0, frame0, cam0_red_min, cam0_red_max, cam0_red_color)
    process_color(lab0, frame0, cam0_yellow_min, cam0_yellow_max, cam0_yellow_color)
    process_color(lab0, frame0, cam0_blue_min, cam0_blue_max, cam0_blue_color)

    # Камера 1
    ball_angle_1 = process_color(lab1, frame1, cam1_red_min, cam1_red_max, cam1_red_color)
    process_color(lab1, frame1, cam1_yellow_min, cam1_yellow_max, cam1_yellow_color)
    process_color(lab1, frame1, cam1_blue_min, cam1_blue_max, cam1_blue_color)

    print(ball_angle_0, ball_angle_1)

    # Отображение
    cv2.imshow('Camera 0 (Front)', frame0)
    cv2.imshow('Camera 1 (Back)', frame1)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam0.stop()
cam1.stop()
cv2.destroyAllWindows()