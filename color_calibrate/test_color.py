import cv2
from picamera2 import Picamera2
import numpy as np
import json
import os

CALIB_FILE = "./color_calibrate/calibration.json"

def nothing(*arg):
    pass

def load_calibration():
    if os.path.exists(CALIB_FILE):
        with open(CALIB_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_calibration(data):
    os.makedirs(os.path.dirname(CALIB_FILE), exist_ok=True)
    with open(CALIB_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def calibrate_color(camera, cam_name, color_name, initial_values=None):
    if initial_values is None:
        initial_values = {'L1':0, 'a1':0, 'b1':0, 'L2':255, 'a2':255, 'b2':255}

    window_name = f"{cam_name}_{color_name}"
    cv2.namedWindow(window_name)

    cv2.createTrackbar('L1', window_name, initial_values['L1'], 255, nothing)
    cv2.createTrackbar('a1', window_name, initial_values['a1'], 255, nothing)
    cv2.createTrackbar('b1', window_name, initial_values['b1'], 255, nothing)
    cv2.createTrackbar('L2', window_name, initial_values['L2'], 255, nothing)
    cv2.createTrackbar('a2', window_name, initial_values['a2'], 255, nothing)
    cv2.createTrackbar('b2', window_name, initial_values['b2'], 255, nothing)

    print(f"Calibrate {color_name.upper()} for {cam_name}. Press 'q' when done.")

    while True:
        img = cv2.cvtColor(cv2.flip(camera.capture_array(), -1), cv2.COLOR_RGB2BGR)
        lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)

        L1 = cv2.getTrackbarPos('L1', window_name)
        a1 = cv2.getTrackbarPos('a1', window_name)
        b1 = cv2.getTrackbarPos('b1', window_name)
        L2 = cv2.getTrackbarPos('L2', window_name)
        a2 = cv2.getTrackbarPos('a2', window_name)
        b2 = cv2.getTrackbarPos('b2', window_name)

        lower = np.array([L1, a1, b1], dtype=np.uint8)
        upper = np.array([L2, a2, b2], dtype=np.uint8)

        mask = cv2.inRange(lab, lower, upper)
        result = cv2.bitwise_and(img, img, mask=mask)

        cv2.imshow(window_name, result)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyWindow(window_name)

    return {'L1': L1, 'a1': a1, 'b1': b1, 'L2': L2, 'a2': a2, 'b2': b2}

def main():
    calib_data = load_calibration()

    cam0 = Picamera2(1)
    cam1 = Picamera2(0)
    config0 = cam0.create_video_configuration(main={"size": (1296, 972)})
    config1 = cam1.create_video_configuration(main={"size": (1296, 972)})
    cam0.configure(config0)
    cam1.configure(config1)

    colors = ['red', 'yellow', 'blue']

    cam0.start()
    for color in colors:
        key = f"cam0_{color}"
        initial = calib_data.get(key, None)
        values = calibrate_color(cam0, "cam0", color, initial)
        calib_data[key] = values
        save_calibration(calib_data)
    cam0.stop()

    cam1.start()
    for color in colors:
        key = f"cam1_{color}"
        initial = calib_data.get(key, None)
        values = calibrate_color(cam1, "cam1", color, initial)
        calib_data[key] = values
        save_calibration(calib_data)
    cam1.stop()

    print("Calibration completed and saved to", CALIB_FILE)

if __name__ == '__main__':
    main()