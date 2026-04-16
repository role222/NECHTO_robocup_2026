import numpy as np
import cv2
from picamera2 import Picamera2

f = open("./color_calibrate/variable.txt", "r")

cam0_red_var = f.readline()
cam0_red_h1 = int(cam0_red_var[0:int(cam0_red_var.find(" "))])
cam0_red_var = cam0_red_var[int(cam0_red_var.find(" ")+1):]
cam0_red_s1 = int(cam0_red_var[0:int(cam0_red_var.find(" "))])
cam0_red_var = cam0_red_var[int(cam0_red_var.find(" ")+1):]
cam0_red_v1 = int(cam0_red_var[0:int(cam0_red_var.find(" "))])
cam0_red_var = cam0_red_var[int(cam0_red_var.find(" ")+1):]
cam0_red_h2 = int(cam0_red_var[0:int(cam0_red_var.find(" "))])
cam0_red_var = cam0_red_var[int(cam0_red_var.find(" ")+1):]
cam0_red_s2 = int(cam0_red_var[0:int(cam0_red_var.find(" "))])
cam0_red_var = cam0_red_var[int(cam0_red_var.find(" ")+1):]
cam0_red_v2 = int(cam0_red_var[0:])

cam0_red_min = np.array((cam0_red_h1, cam0_red_s1, cam0_red_v1), np.uint8)
cam0_red_max = np.array((cam0_red_h2, cam0_red_s2, cam0_red_v2), np.uint8)

# среднее ограничений для красного и противоположный цвет для круга
cam0_red_mean_hsv = ((cam0_red_min.astype(np.int32) + cam0_red_max.astype(np.int32)) // 2).astype(np.uint8)
cam0_red_comp_h = int((int(cam0_red_mean_hsv[0]) + 90) % 180)   
cam0_red_comp_hsv = np.array([[[cam0_red_comp_h, int(cam0_red_mean_hsv[1]), int(cam0_red_mean_hsv[2])]]], np.uint8)
cam0_red_circle_color = tuple(int(c) for c in cv2.cvtColor(cam0_red_comp_hsv, cv2.COLOR_HSV2BGR)[0,0])

cam0_yellow_var = f.readline()
cam0_yellow_h1 = int(cam0_yellow_var[0:int(cam0_yellow_var.find(" "))])
cam0_yellow_var = cam0_yellow_var[int(cam0_yellow_var.find(" ")+1):]
cam0_yellow_s1 = int(cam0_yellow_var[0:int(cam0_yellow_var.find(" "))])
cam0_yellow_var = cam0_yellow_var[int(cam0_yellow_var.find(" ")+1):]
cam0_yellow_v1 = int(cam0_yellow_var[0:int(cam0_yellow_var.find(" "))])
cam0_yellow_var = cam0_yellow_var[int(cam0_yellow_var.find(" ")+1):]
cam0_yellow_h2 = int(cam0_yellow_var[0:int(cam0_yellow_var.find(" "))])
cam0_yellow_var = cam0_yellow_var[int(cam0_yellow_var.find(" ")+1):]
cam0_yellow_s2 = int(cam0_yellow_var[0:int(cam0_yellow_var.find(" "))])
cam0_yellow_var = cam0_yellow_var[int(cam0_yellow_var.find(" ")+1):]
cam0_yellow_v2 = int(cam0_yellow_var[0:])

cam0_yellow_min = np.array((cam0_yellow_h1, cam0_yellow_s1, cam0_yellow_v1), np.uint8)
cam0_yellow_max = np.array((cam0_yellow_h2, cam0_yellow_s2, cam0_yellow_v2), np.uint8)

# среднее ограничений для красного и противоположный цвет для круга
cam0_yellow_mean_hsv = ((cam0_yellow_min.astype(np.int32) + cam0_yellow_max.astype(np.int32)) // 2).astype(np.uint8)
cam0_yellow_comp_h = int((int(cam0_yellow_mean_hsv[0]) + 90) % 180)   
cam0_yellow_comp_hsv = np.array([[[cam0_yellow_comp_h, int(cam0_yellow_mean_hsv[1]), int(cam0_yellow_mean_hsv[2])]]], np.uint8)
cam0_yellow_circle_color = tuple(int(c) for c in cv2.cvtColor(cam0_yellow_comp_hsv, cv2.COLOR_HSV2BGR)[0,0])

cam0_blue_var = f.readline()
cam0_blue_h1 = int(cam0_blue_var[0:int(cam0_blue_var.find(" "))])
cam0_blue_var = cam0_blue_var[int(cam0_blue_var.find(" ")+1):]
cam0_blue_s1 = int(cam0_blue_var[0:int(cam0_blue_var.find(" "))])
cam0_blue_var = cam0_blue_var[int(cam0_blue_var.find(" ")+1):]
cam0_blue_v1 = int(cam0_blue_var[0:int(cam0_blue_var.find(" "))])
cam0_blue_var = cam0_blue_var[int(cam0_blue_var.find(" ")+1):]
cam0_blue_h2 = int(cam0_blue_var[0:int(cam0_blue_var.find(" "))])
cam0_blue_var = cam0_blue_var[int(cam0_blue_var.find(" ")+1):]
cam0_blue_s2 = int(cam0_blue_var[0:int(cam0_blue_var.find(" "))])
cam0_blue_var = cam0_blue_var[int(cam0_blue_var.find(" ")+1):]
cam0_blue_v2 = int(cam0_blue_var[0:])

cam0_blue_min = np.array((cam0_blue_h1, cam0_blue_s1, cam0_blue_v1), np.uint8)
cam0_blue_max = np.array((cam0_blue_h2, cam0_blue_s2, cam0_blue_v2), np.uint8)

# среднее ограничений для красного и противоположный цвет для круга
cam0_blue_mean_hsv = ((cam0_blue_min.astype(np.int32) + cam0_blue_max.astype(np.int32)) // 2).astype(np.uint8)
cam0_blue_comp_h = int((int(cam0_blue_mean_hsv[0]) + 90) % 180)   
cam0_blue_comp_hsv = np.array([[[cam0_blue_comp_h, int(cam0_blue_mean_hsv[1]), int(cam0_blue_mean_hsv[2])]]], np.uint8)
cam0_blue_circle_color = tuple(int(c) for c in cv2.cvtColor(cam0_blue_comp_hsv, cv2.COLOR_HSV2BGR)[0,0])

cam1_red_var = f.readline()
cam1_red_h1 = int(cam1_red_var[0:int(cam1_red_var.find(" "))])
cam1_red_var = cam1_red_var[int(cam1_red_var.find(" ")+1):]
cam1_red_s1 = int(cam1_red_var[0:int(cam1_red_var.find(" "))])
cam1_red_var = cam1_red_var[int(cam1_red_var.find(" ")+1):]
cam1_red_v1 = int(cam1_red_var[0:int(cam1_red_var.find(" "))])
cam1_red_var = cam1_red_var[int(cam1_red_var.find(" ")+1):]
cam1_red_h2 = int(cam1_red_var[0:int(cam1_red_var.find(" "))])
cam1_red_var = cam1_red_var[int(cam1_red_var.find(" ")+1):]
cam1_red_s2 = int(cam1_red_var[0:int(cam1_red_var.find(" "))])
cam1_red_var = cam1_red_var[int(cam1_red_var.find(" ")+1):]
cam1_red_v2 = int(cam1_red_var[0:])

cam1_red_min = np.array((cam1_red_h1, cam1_red_s1, cam1_red_v1), np.uint8)
cam1_red_max = np.array((cam1_red_h2, cam1_red_s2, cam1_red_v2), np.uint8)

# среднее ограничений для красного и противоположный цвет для круга
cam1_red_mean_hsv = ((cam1_red_min.astype(np.int32) + cam1_red_max.astype(np.int32)) // 2).astype(np.uint8)
cam1_red_comp_h = int((int(cam1_red_mean_hsv[0]) + 90) % 180)   
cam1_red_comp_hsv = np.array([[[cam1_red_comp_h, int(cam1_red_mean_hsv[1]), int(cam1_red_mean_hsv[2])]]], np.uint8)
cam1_red_circle_color = tuple(int(c) for c in cv2.cvtColor(cam1_red_comp_hsv, cv2.COLOR_HSV2BGR)[0,0])

cam1_yellow_var = f.readline()
cam1_yellow_h1 = int(cam1_yellow_var[0:int(cam1_yellow_var.find(" "))])
cam1_yellow_var = cam1_yellow_var[int(cam1_yellow_var.find(" ")+1):]
cam1_yellow_s1 = int(cam1_yellow_var[0:int(cam1_yellow_var.find(" "))])
cam1_yellow_var = cam1_yellow_var[int(cam1_yellow_var.find(" ")+1):]
cam1_yellow_v1 = int(cam1_yellow_var[0:int(cam1_yellow_var.find(" "))])
cam1_yellow_var = cam1_yellow_var[int(cam1_yellow_var.find(" ")+1):]
cam1_yellow_h2 = int(cam1_yellow_var[0:int(cam1_yellow_var.find(" "))])
cam1_yellow_var = cam1_yellow_var[int(cam1_yellow_var.find(" ")+1):]
cam1_yellow_s2 = int(cam1_yellow_var[0:int(cam1_yellow_var.find(" "))])
cam1_yellow_var = cam1_yellow_var[int(cam1_yellow_var.find(" ")+1):]
cam1_yellow_v2 = int(cam1_yellow_var[0:])

cam1_yellow_min = np.array((cam1_yellow_h1, cam1_yellow_s1, cam1_yellow_v1), np.uint8)
cam1_yellow_max = np.array((cam1_yellow_h2, cam1_yellow_s2, cam1_yellow_v2), np.uint8)

# среднее ограничений для красного и противоположный цвет для круга
cam1_yellow_mean_hsv = ((cam1_yellow_min.astype(np.int32) + cam1_yellow_max.astype(np.int32)) // 2).astype(np.uint8)
cam1_yellow_comp_h = int((int(cam1_yellow_mean_hsv[0]) + 90) % 180)   
cam1_yellow_comp_hsv = np.array([[[cam1_yellow_comp_h, int(cam1_yellow_mean_hsv[1]), int(cam1_yellow_mean_hsv[2])]]], np.uint8)
cam1_yellow_circle_color = tuple(int(c) for c in cv2.cvtColor(cam1_yellow_comp_hsv, cv2.COLOR_HSV2BGR)[0,0])

cam1_blue_var = f.readline()
cam1_blue_h1 = int(cam1_blue_var[0:int(cam1_blue_var.find(" "))])
cam1_blue_var = cam1_blue_var[int(cam1_blue_var.find(" ")+1):]
cam1_blue_s1 = int(cam1_blue_var[0:int(cam1_blue_var.find(" "))])
cam1_blue_var = cam1_blue_var[int(cam1_blue_var.find(" ")+1):]
cam1_blue_v1 = int(cam1_blue_var[0:int(cam1_blue_var.find(" "))])
cam1_blue_var = cam1_blue_var[int(cam1_blue_var.find(" ")+1):]
cam1_blue_h2 = int(cam1_blue_var[0:int(cam1_blue_var.find(" "))])
cam1_blue_var = cam1_blue_var[int(cam1_blue_var.find(" ")+1):]
cam1_blue_s2 = int(cam1_blue_var[0:int(cam1_blue_var.find(" "))])
cam1_blue_var = cam1_blue_var[int(cam1_blue_var.find(" ")+1):]
cam1_blue_v2 = int(cam1_blue_var[0:])

cam1_blue_min = np.array((cam1_blue_h1, cam1_blue_s1, cam1_blue_v1), np.uint8)
cam1_blue_max = np.array((cam1_blue_h2, cam1_blue_s2, cam1_blue_v2), np.uint8)

# среднее ограничений для красного и противоположный цвет для круга
cam1_blue_mean_hsv = ((cam1_blue_min.astype(np.int32) + cam1_blue_max.astype(np.int32)) // 2).astype(np.uint8)
cam1_blue_comp_h = int((int(cam1_blue_mean_hsv[0]) + 90) % 180)   
cam1_blue_comp_hsv = np.array([[[cam1_blue_comp_h, int(cam1_blue_mean_hsv[1]), int(cam1_blue_mean_hsv[2])]]], np.uint8)
cam1_blue_circle_color = tuple(int(c) for c in cv2.cvtColor(cam1_blue_comp_hsv, cv2.COLOR_HSV2BGR)[0,0])

cam0 = Picamera2(0)
cam1 = Picamera2(1)
config0 = cam0.create_video_configuration(main={"size": (1296, 972)})
config1 = cam1.create_video_configuration(main={"size": (1296, 972)})
cam0.configure(config0)
cam1.configure(config1)
cam0.start()
cam1.start()

while True:
    frame0 = cv2.cvtColor(cv2.flip(cam0.capture_array(), -1),cv2.COLOR_RGB2BGR)
    frame1 = cv2.cvtColor(cv2.flip(cam1.capture_array(), -1),cv2.COLOR_RGB2BGR)

    hsv_0 = cv2.cvtColor(frame0, cv2.COLOR_BGR2HSV )
    hsv_1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2HSV )
    
    cam0_red_image = cv2.inRange(hsv_0, cam0_red_min, cam0_red_max)
    cam0_red_m = cv2.moments(cam0_red_image, 1)
    cam0_red_01 = cam0_red_m['m01']
    cam0_red_10 = cam0_red_m['m10']
    cam0_red_Area = cam0_red_m['m00']
    if cam0_red_Area > 100:
        cam0_red_x = int(cam0_red_10 / cam0_red_Area)
        cam0_red_y = int(cam0_red_01 / cam0_red_Area)
        cv2.circle(frame0, (int(cam0_red_x), int(cam0_red_y)), 10, cam0_red_circle_color, -1)

    cam0_yellow_image = cv2.inRange(hsv_0, cam0_yellow_min, cam0_yellow_max)
    cam0_yellow_m = cv2.moments(cam0_yellow_image, 1)
    cam0_yellow_01 = cam0_yellow_m['m01']
    cam0_yellow_10 = cam0_yellow_m['m10']
    cam0_yellow_Area = cam0_yellow_m['m00']
    if cam0_yellow_Area > 100:
        cam0_yellow_x = int(cam0_yellow_10 / cam0_yellow_Area)
        cam0_yellow_y = int(cam0_yellow_01 / cam0_yellow_Area)
        cv2.circle(frame0, (int(cam0_yellow_x), int(cam0_yellow_y)), 10, cam0_yellow_circle_color, -1)

    cam0_blue_image = cv2.inRange(hsv_0, cam0_blue_min, cam0_blue_max)
    cam0_blue_m = cv2.moments(cam0_blue_image, 1)
    cam0_blue_01 = cam0_blue_m['m01']
    cam0_blue_10 = cam0_blue_m['m10']
    cam0_blue_Area = cam0_blue_m['m00']
    if cam0_blue_Area > 100:
        cam0_blue_x = int(cam0_blue_10 / cam0_blue_Area)
        cam0_blue_y = int(cam0_blue_01 / cam0_blue_Area)
        cv2.circle(frame0, (int(cam0_blue_x), int(cam0_blue_y)), 10, cam0_blue_circle_color, -1)

    cam1_red_image = cv2.inRange(hsv_1, cam1_red_min, cam1_red_max)
    cam1_red_m = cv2.moments(cam1_red_image, 1)
    cam1_red_01 = cam1_red_m['m01']
    cam1_red_10 = cam1_red_m['m10']
    cam1_red_Area = cam1_red_m['m00']
    if cam1_red_Area > 100:
        cam1_red_x = int(cam1_red_10 / cam1_red_Area)
        cam1_red_y = int(cam1_red_01 / cam1_red_Area)
        cv2.circle(frame1, (int(cam1_red_x), int(cam1_red_y)), 10, cam1_red_circle_color, -1)

    cam1_yellow_image = cv2.inRange(hsv_1, cam1_yellow_min, cam1_yellow_max)
    cam1_yellow_m = cv2.moments(cam1_yellow_image, 1)
    cam1_yellow_01 = cam1_yellow_m['m01']
    cam1_yellow_10 = cam1_yellow_m['m10']
    cam1_yellow_Area = cam1_yellow_m['m00']
    if cam1_yellow_Area > 100:
        cam1_yellow_x = int(cam1_yellow_10 / cam1_yellow_Area)
        cam1_yellow_y = int(cam1_yellow_01 / cam1_yellow_Area)
        cv2.circle(frame1, (int(cam1_yellow_x), int(cam1_yellow_y)), 10, cam1_yellow_circle_color, -1)

    cam1_blue_image = cv2.inRange(hsv_1, cam1_blue_min, cam1_blue_max)
    cam1_blue_m = cv2.moments(cam1_blue_image, 1)
    cam1_blue_01 = cam1_blue_m['m01']
    cam1_blue_10 = cam1_blue_m['m10']
    cam1_blue_Area = cam1_blue_m['m00']
    if cam1_blue_Area > 100:
        cam1_blue_x = int(cam1_blue_10 / cam1_blue_Area)
        cam1_blue_y = int(cam1_blue_01 / cam1_blue_Area)
        cv2.circle(frame1, (int(cam1_blue_x), int(cam1_blue_y)), 10, cam1_blue_circle_color, -1)

    cv2.imshow('Camera 0 (Front)', frame0)
    cv2.imshow('Camera 1 (Back)', frame1)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam0.stop()
cam1.stop()
cv2.destroyAllWindows()