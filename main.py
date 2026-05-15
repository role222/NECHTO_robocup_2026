import pyb
import struct
import sensor
import image
import time
import math

frame_counter = 0

# ── Настройка камеры ──
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.SVGA)                     # 640×480
sensor.set_windowing(257,187,320,320)
sensor.skip_frames(time=2000)
sensor.set_auto_gain(False)
sensor.set_auto_whitebal(False)
sensor.set_auto_exposure(False)
sensor.set_hmirror(False)
sensor.set_vflip(False)
#sensor.set_brightness(-3)

print("Resolution:", sensor.width(), "x", sensor.height())

# ── Геометрия кольца (раздельные центры) ──
CENTER_OUTER_X = 160    # центр внешней окружности (ось вращения)
CENTER_OUTER_Y = 160
RING_OUTER     = 200    # внешний радиус

CENTER_INNER_X = 160    # центр внутреннего круга (можно сдвинуть)
CENTER_INNER_Y = 168
RING_INNER     = 65     # внутренний радиус

# Толщина чёрного кольца, чтобы перекрыть всё за пределами RING_OUTER
# Вычисляется с запасом от радиуса до угла кадра
MASK_THICKNESS = 90  # 640 – точно перекроет всё снаружи

# ── Цветовые пороги (LAB) ──

#YELLOW_THRESHOLD  = (77, 100, -35, 27, 22, 127)
#ORANGE_THRESHOLD  = (35, 83, 11, 48, 5, 29)
#BLUE_THRESHOLD    = (0, 100, -32, 21, -81, -24)

YELLOW_THRESHOLD  = (77, 100, -35, 27, 22, 127)
ORANGE_THRESHOLD  = (35, 83, 11, 48, 5, 29)
BLUE_THRESHOLD    = (0, 100, -32, 21, -81, -24)

# ── Константы ──
ANGLE_NONE = 0x0000
RAD_TO_DEG = 57.2957795
CIRCLE_360 = 360.0

# ── I2C slave ──
bus = pyb.I2C(2, pyb.I2C.SLAVE, addr=0x12)
bus.deinit()
bus = pyb.I2C(2, pyb.I2C.SLAVE, addr=0x12)
print("Waiting for Arduino...")

clock = time.clock()
packet_buffer = bytearray(6)

def calculate_angle(cx, cy):
    dx = cx - CENTER_OUTER_X
    dy = cy - CENTER_OUTER_Y
    return int((math.atan2(dy, dx) * RAD_TO_DEG + CIRCLE_360) % CIRCLE_360)

# ── Основной цикл ──
while True:
    clock.tick()
    img = sensor.snapshot()

    # ═══ ЗАМЕНА mask_circle: рисуем толстое чёрное кольцо снаружи ═══
    img.draw_circle(CENTER_OUTER_X, CENTER_OUTER_Y, RING_OUTER,
                    color=(0, 0, 0), thickness=MASK_THICKNESS)

    # Внутренний круг (чёрная заливка) — всегда
    img.draw_circle(CENTER_INNER_X, CENTER_INNER_Y, RING_INNER,
                    color=(0, 0, 0), fill=True)

    # Поиск блобов по всему кадру (всё лишнее уже закрашено чёрным)
    all_blobs = img.find_blobs(
        [YELLOW_THRESHOLD, ORANGE_THRESHOLD, BLUE_THRESHOLD],
        pixels_threshold=10,
        area_threshold=10,
        merge=False,
        margin=5
    )

    # Выбор крупнейших блобов каждого цвета
    best_y = best_o = best_b = None
    max_area_y = max_area_o = max_area_b = 0

    for b in all_blobs:
        code = b.code()
        area = b.area()
        if code & 1 and area > max_area_y:
            max_area_y = area
            best_y = b
        elif code & 2 and area > max_area_o:
            max_area_o = area
            best_o = b
        elif code & 4 and area > max_area_b:
            max_area_b = area
            best_b = b

    # Вычисление углов
    angle_y = angle_o = angle_b = ANGLE_NONE

    if best_y:
        cx, cy = best_y.cx(), best_y.cy()
        img.draw_cross(cx, cy, color=(0, 255, 0), size=8)
        angle_y = calculate_angle(cx, cy)

    if best_o:
        cx, cy = best_o.cx(), best_o.cy()
        img.draw_cross(cx, cy, color=(0, 0, 255), size=8)
        angle_o = calculate_angle(cx, cy)

    if best_b:
        cx, cy = best_b.cx(), best_b.cy()
        img.draw_cross(cx, cy, color=(255, 0, 0), size=8)
        angle_b = calculate_angle(cx, cy)

    # I2C передача
    struct.pack_into('<HHH', packet_buffer, 0, angle_o, angle_y, angle_b)
    try:
        bus.send(packet_buffer, timeout=1)
    except OSError:
        pass

    frame_counter += 1
    if frame_counter % 30 == 0:
        print("Y:%d O:%d B:%d | FPS:%d" % (angle_y, angle_o, angle_b, clock.fps()))
