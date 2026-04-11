import cv2
from picamera2 import Picamera2
import numpy as np
import os
os.system(r"rm -rf ./color_calibrate/variable.txt")
if __name__ == '__main__':
    def nothing(*arg):
        pass

cam0 = Picamera2(0)
cam1 = Picamera2(1)
config0 = cam0.create_video_configuration(main={"size": (1296, 972)})
config1 = cam1.create_video_configuration(main={"size": (1296, 972)})
cam0.configure(config0)
cam1.configure(config1)
cam0.start()

cv2.namedWindow( "settings" )

cap = cv2.VideoCapture(0)

cv2.createTrackbar('h1', 'settings', 0, 255, nothing)
cv2.createTrackbar('s1', 'settings', 0, 255, nothing)
cv2.createTrackbar('v1', 'settings', 0, 255, nothing)
cv2.createTrackbar('h2', 'settings', 0, 255, nothing)
cv2.createTrackbar('s2', 'settings', 0, 255, nothing)
cv2.createTrackbar('v2', 'settings', 0, 255, nothing)

h1 = 0
s1 = 0
v1 = 0
h2 = 0
s2 = 0
v2 = 0


while True:
    img = cv2.cvtColor(cv2.flip(cam0.capture_array(), -1),cv2.COLOR_RGB2BGR)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV )
 
    h1 = cv2.getTrackbarPos('h1', 'settings')
    s1 = cv2.getTrackbarPos('s1', 'settings')
    v1 = cv2.getTrackbarPos('v1', 'settings')
    h2 = cv2.getTrackbarPos('h2', 'settings')
    s2 = cv2.getTrackbarPos('s2', 'settings')
    v2 = cv2.getTrackbarPos('v2', 'settings')

    h_min = np.array((h1, s1, v1), np.uint8)
    h_max = np.array((h2, s2, v2), np.uint8)

    thresh = cv2.inRange(hsv, h_min, h_max)

    cv2.imshow('RED_result', thresh) 
    cv2.imshow('RED_image', img) 
 
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()

f = open(r'./color_calibrate/variable.txt', 'w')
f.write(str(str(h1) + ' ' + str(s1) + ' ' + str(v1) + ' ' + str(h2) + ' ' + str(s2) + ' ' + str(v2) + "\n"))

cv2.namedWindow( "settings" )

cv2.createTrackbar('h1', 'settings', 0, 255, nothing)
cv2.createTrackbar('s1', 'settings', 0, 255, nothing)
cv2.createTrackbar('v1', 'settings', 0, 255, nothing)
cv2.createTrackbar('h2', 'settings', 0, 255, nothing)
cv2.createTrackbar('s2', 'settings', 0, 255, nothing)
cv2.createTrackbar('v2', 'settings', 0, 255, nothing)

h1 = 0
s1 = 0
v1 = 0
h2 = 0
s2 = 0
v2 = 0

while True:
    img = cv2.cvtColor(cv2.flip(cam0.capture_array(), -1),cv2.COLOR_RGB2BGR)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV )
 
    h1 = cv2.getTrackbarPos('h1', 'settings')
    s1 = cv2.getTrackbarPos('s1', 'settings')
    v1 = cv2.getTrackbarPos('v1', 'settings')
    h2 = cv2.getTrackbarPos('h2', 'settings')
    s2 = cv2.getTrackbarPos('s2', 'settings')
    v2 = cv2.getTrackbarPos('v2', 'settings')

    h_min = np.array((h1, s1, v1), np.uint8)
    h_max = np.array((h2, s2, v2), np.uint8)

    thresh = cv2.inRange(hsv, h_min, h_max)

    cv2.imshow('YELLOW_result', thresh) 
    cv2.imshow('YELLOW_image', img) 
 
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()
f.write(str(str(h1) + ' ' + str(s1) + ' ' + str(v1) + ' ' + str(h2) + ' ' + str(s2) + ' ' + str(v2) + "\n"))

cv2.namedWindow( "settings" )
cv2.createTrackbar('h1', 'settings', 0, 255, nothing)
cv2.createTrackbar('s1', 'settings', 0, 255, nothing)
cv2.createTrackbar('v1', 'settings', 0, 255, nothing)
cv2.createTrackbar('h2', 'settings', 0, 255, nothing)
cv2.createTrackbar('s2', 'settings', 0, 255, nothing)
cv2.createTrackbar('v2', 'settings', 0, 255, nothing)
while True:
    img = cv2.cvtColor(cv2.flip(cam0.capture_array(), -1),cv2.COLOR_RGB2BGR)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV )
 
    h1 = cv2.getTrackbarPos('h1', 'settings')
    s1 = cv2.getTrackbarPos('s1', 'settings')
    v1 = cv2.getTrackbarPos('v1', 'settings')
    h2 = cv2.getTrackbarPos('h2', 'settings')
    s2 = cv2.getTrackbarPos('s2', 'settings')
    v2 = cv2.getTrackbarPos('v2', 'settings')

    h_min = np.array((h1, s1, v1), np.uint8)
    h_max = np.array((h2, s2, v2), np.uint8)

    thresh = cv2.inRange(hsv, h_min, h_max)

    cv2.imshow('BLUE_result', thresh) 
    cv2.imshow('BLUE_image', img) 
 
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()
f.write(str(str(h1) + ' ' + str(s1) + ' ' + str(v1) + ' ' + str(h2) + ' ' + str(s2) + ' ' + str(v2) + "\n"))
cam0.stop()


cam1.start()
while True:
    img = cv2.cvtColor(cv2.flip(cam1.capture_array(), -1),cv2.COLOR_RGB2BGR)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV )
 
    h1 = cv2.getTrackbarPos('h1', 'settings')
    s1 = cv2.getTrackbarPos('s1', 'settings')
    v1 = cv2.getTrackbarPos('v1', 'settings')
    h2 = cv2.getTrackbarPos('h2', 'settings')
    s2 = cv2.getTrackbarPos('s2', 'settings')
    v2 = cv2.getTrackbarPos('v2', 'settings')

    h_min = np.array((h1, s1, v1), np.uint8)
    h_max = np.array((h2, s2, v2), np.uint8)

    thresh = cv2.inRange(hsv, h_min, h_max)

    cv2.imshow('RED_result', thresh) 
    cv2.imshow('RED_image', img) 
 
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()

f = open(r'./color_calibrate/variable.txt', 'w')
f.write(str(str(h1) + ' ' + str(s1) + ' ' + str(v1) + ' ' + str(h2) + ' ' + str(s2) + ' ' + str(v2) + "\n"))

cv2.namedWindow( "settings" )

cv2.createTrackbar('h1', 'settings', 0, 255, nothing)
cv2.createTrackbar('s1', 'settings', 0, 255, nothing)
cv2.createTrackbar('v1', 'settings', 0, 255, nothing)
cv2.createTrackbar('h2', 'settings', 0, 255, nothing)
cv2.createTrackbar('s2', 'settings', 0, 255, nothing)
cv2.createTrackbar('v2', 'settings', 0, 255, nothing)

h1 = 0
s1 = 0
v1 = 0
h2 = 0
s2 = 0
v2 = 0

while True:
    img = cv2.cvtColor(cv2.flip(cam1.capture_array(), -1),cv2.COLOR_RGB2BGR)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV )
 
    h1 = cv2.getTrackbarPos('h1', 'settings')
    s1 = cv2.getTrackbarPos('s1', 'settings')
    v1 = cv2.getTrackbarPos('v1', 'settings')
    h2 = cv2.getTrackbarPos('h2', 'settings')
    s2 = cv2.getTrackbarPos('s2', 'settings')
    v2 = cv2.getTrackbarPos('v2', 'settings')

    h_min = np.array((h1, s1, v1), np.uint8)
    h_max = np.array((h2, s2, v2), np.uint8)

    thresh = cv2.inRange(hsv, h_min, h_max)

    cv2.imshow('YELLOW_result', thresh) 
    cv2.imshow('YELLOW_image', img) 
 
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()
f.write(str(str(h1) + ' ' + str(s1) + ' ' + str(v1) + ' ' + str(h2) + ' ' + str(s2) + ' ' + str(v2) + "\n"))

cv2.namedWindow( "settings" )
cv2.createTrackbar('h1', 'settings', 0, 255, nothing)
cv2.createTrackbar('s1', 'settings', 0, 255, nothing)
cv2.createTrackbar('v1', 'settings', 0, 255, nothing)
cv2.createTrackbar('h2', 'settings', 0, 255, nothing)
cv2.createTrackbar('s2', 'settings', 0, 255, nothing)
cv2.createTrackbar('v2', 'settings', 0, 255, nothing)
while True:
    img = cv2.cvtColor(cv2.flip(cam1.capture_array(), -1),cv2.COLOR_RGB2BGR)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV )
 
    h1 = cv2.getTrackbarPos('h1', 'settings')
    s1 = cv2.getTrackbarPos('s1', 'settings')
    v1 = cv2.getTrackbarPos('v1', 'settings')
    h2 = cv2.getTrackbarPos('h2', 'settings')
    s2 = cv2.getTrackbarPos('s2', 'settings')
    v2 = cv2.getTrackbarPos('v2', 'settings')

    h_min = np.array((h1, s1, v1), np.uint8)
    h_max = np.array((h2, s2, v2), np.uint8)

    thresh = cv2.inRange(hsv, h_min, h_max)

    cv2.imshow('BLUE_result', thresh) 
    cv2.imshow('BLUE_image', img) 
 
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()
f.write(str(str(h1) + ' ' + str(s1) + ' ' + str(v1) + ' ' + str(h2) + ' ' + str(s2) + ' ' + str(v2) + "\n"))
cam1.stop()

f.close()