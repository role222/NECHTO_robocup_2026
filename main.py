import sensor, image, time, pyb, struct, math

# ==================== НАСТРОЙКА КАМЕРЫ ====================
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.HVGA)          # 480×320 до трансформации

sensor.set_hmirror(True)
sensor.set_vflip(True)
sensor.set_transpose(True)

sensor.set_auto_whitebal(False)
sensor.set_auto_gain(False)
sensor.skip_frames(time=2000)
clock = time.clock()

# ==================== ПАРАМЕТРЫ ЗЕРКАЛА ====================
CENTER_X   = 160
CENTER_Y   = 240
RING_RADIUS = 140

# ==================== ЦВЕТОВЫЕ ПОРОГИ (LAB) ====================
THR_RED    = (30, 100, 15, 127, 15, 127)   # пример – настройте по своим меткам
THR_YELLOW = (50, 100, -10, 10, 20, 127)
THR_BLUE   = (10, 60, -128, -20, -30, 30)

# ==================== I2C SLAVE ====================
bus = pyb.I2C(2, pyb.I2C.SLAVE, addr=0x12)
bus.deinit()
bus = pyb.I2C(2, pyb.I2C.SLAVE, addr=0x12)

# ==================== UART для вывода углов и FPS ====================
uart = pyb.UART(3, 921600)   # P0 (TX) / P1 (RX) на OpenMV H7
uart.init(921600, bits=8, parity=None, stop=1)

print("Waiting for Arduino... (angles on UART)")

# ==================== ФУНКЦИЯ УГЛА ====================
def get_angle(x, y, cx, cy):
    dx = x - cx
    dy = y - cy
    angle = math.degrees(math.atan2(dx, -dy))  # 0° – вверх по изображению
    return (angle + 360) % 360

# ==================== ОСНОВНОЙ ЦИКЛ ====================
while True:
    clock.tick()
    img = sensor.snapshot()

    # ---------- ОТЛАДОЧНАЯ ОТРИСОВКА (можно убрать для ускорения) ----------
    # img.draw_cross(CENTER_X, CENTER_Y, size=10, color=(255,255,255))
    # img.draw_circle(CENTER_X, CENTER_Y, RING_RADIUS, color=(255,255,255))
    # img.draw_line(CENTER_X, CENTER_Y, CENTER_X, CENTER_Y - 30, color=(0,255,0))
    # ---------------------------------------------------------------------

    # --- Поиск всех трёх цветов за один проход ---
    blobs = img.find_blobs([THR_RED, THR_YELLOW, THR_BLUE],
                           pixels_threshold=20, area_threshold=20,
                           merge=True)  # merge=True склеивает близкие области

    # Разделяем по коду цвета (0 – красный, 1 – жёлтый, 2 – синий)
    red_blobs    = [b for b in blobs if b.code() == 1]   # code 1 для первого порога
    yellow_blobs = [b for b in blobs if b.code() == 2]
    blue_blobs   = [b for b in blobs if b.code() == 4]   # битовая маска: 1,2,4

    # Берём самый крупный блоб каждого цвета (если есть)
    largest_red    = red_blobs[0]    if red_blobs    else None
    largest_yellow = yellow_blobs[0] if yellow_blobs else None
    largest_blue   = blue_blobs[0]   if blue_blobs   else None

    # --- Вычисляем углы ---
    angles = []
    for blob, label in [(largest_red, "R"), (largest_yellow, "Y"), (largest_blue, "B")]:
        if blob:
            x, y = blob.cx(), blob.cy()
            ang = int(round(get_angle(x, y, CENTER_X, CENTER_Y)))
            angles.append(ang)
            # отрисовка угла на изображении (можно убрать)
            # img.draw_string(x, y, str(ang), color=(255,255,255))
        else:
            angles.append(-1)

    # --- Отправка по I2C ---
    data = struct.pack("<3h", angles[0], angles[1], angles[2])
    try:
        bus.send(struct.pack("<h", len(data)), timeout=10000)
        try:
            bus.send(data, timeout=10000)
        except OSError:
            pass
    except OSError:
        pass

    # --- Вывод углов и FPS в UART (не блокирует) ---
    fps = clock.fps()
    # Формат: "R,Y,B,fps\n" (например "45,123,270,28\n")
    uart.write(f"{angles[0]},{angles[1]},{angles[2]},{fps}\n")