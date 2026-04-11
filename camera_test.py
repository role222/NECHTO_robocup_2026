import cv2
from picamera2 import Picamera2

# Инициализируем объекты для обеих камер
cam0 = Picamera2(0) # Индекс 0 для первого порта
cam1 = Picamera2(1) # Индекс 1 для второго порта

# Конфигурируем обе (например, 640x480)
config0 = cam0.create_video_configuration(main={"size": (1296, 972)})
config1 = cam1.create_video_configuration(main={"size": (1296, 972)})

cam0.configure(config0)
cam1.configure(config1)

# Запуск потоков
cam0.start()
cam1.start()

try:
    while True:
        # Получаем кадры как массивы NumPy
        frame0 = cv2.cvtColor(cv2.flip(cam0.capture_array(), -1),cv2.COLOR_RGB2BGR)
        frame1 = cv2.cvtColor(cv2.flip(cam1.capture_array(), -1),cv2.COLOR_RGB2BGR)

        # Отображаем
        cv2.imshow('Camera 0 (Front)', frame0)
        cv2.imshow('Camera 1 (Back)', frame1)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    cam0.stop()
    cam1.stop()
    cv2.destroyAllWindows()
