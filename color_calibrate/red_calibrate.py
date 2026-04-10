#{"h1": 174, "s1": 34, "v1": 0, "h2": 255, "s2": 255, "v2": 255}
import cv2
import numpy as np
import json
import Ball
import Settings
if __name__ == '__main__':
    def nothing(*arg):
        pass


capList=[0, 1]


cv2.namedWindow("result")  # создаем главное окно
cv2.namedWindow("settings")  # создаем окно настроек
cv2.namedWindow("Cap_Select")
#

#
# создаем 6 бегунков для настройки начального и конечного цвета фильтра
cv2.createTrackbar('h1', 'settings', 0, 255, nothing)
cv2.createTrackbar('s1', 'settings', 0, 255, nothing)
cv2.createTrackbar('v1', 'settings', 0, 255, nothing)
cv2.createTrackbar('h2', 'settings', 255, 255, nothing)
cv2.createTrackbar('s2', 'settings', 255, 255, nothing)
cv2.createTrackbar('v2', 'settings', 255, 255, nothing)
settings=Settings.read()
cv2.setTrackbarPos("h1", "settings", settings.h1)
cv2.setTrackbarPos("s1", "settings", settings.s1)
cv2.setTrackbarPos("v1", "settings", settings.v1)
cv2.setTrackbarPos("h2", "settings", settings.h2)
cv2.setTrackbarPos("s2", "settings", settings.s2)
cv2.setTrackbarPos("v2", "settings", settings.v2)
crange = [0, 0, 0, 0, 0, 0]
cap=cv2.VideoCapture("/dev/video2", cv2.CAP_V4L2)

cap.set(cv2.CAP_PROP_BRIGHTNESS, 140)
settings_file=open("red_1.json", "wb")
while True:
    ret, img=cap.read()#cv2.imread("tests/redball1.jpg")
    if(not ret):
        print('Unable to receive new frame from videocapture')
        continue
    else: previmg=img
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # считываем значения бегунков
    h1 = cv2.getTrackbarPos('h1', 'settings')
    s1 = cv2.getTrackbarPos('s1', 'settings')
    v1 = cv2.getTrackbarPos('v1', 'settings')
    h2 = cv2.getTrackbarPos('h2', 'settings')
    s2 = cv2.getTrackbarPos('s2', 'settings')
    v2 = cv2.getTrackbarPos('v2', 'settings')
    data_array={"h1": h1, "s1": s1, "v1": v1, "h2": h2, "s2": s2, "v2": v2}
    # формируем начальный и конечный цвет фильтра
    h_min = np.array((h1, s1, v1), np.uint8)
    h_max = np.array((h2, s2, v2), np.uint8)
    # накладываем фильтр на кадр в модели HSV
    ball=Ball.Ball(h_min, h_max, thresh_window=True)
    ball.detectBall(img, True)
    cv2.imshow('result', img)
    ch = cv2.waitKey(5)
    if ch == 27:
        settings_file.write(json.dumps(data_array).encode())
        settings_file.close()
        break
cap.release()
cv2.destroyAllWindows()