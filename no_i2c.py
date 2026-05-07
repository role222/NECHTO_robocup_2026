import sensor, image, time, math

# ==================== НАСТРОЙКА КАМЕРЫ ====================
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)          # 480×320 до трансформации

# Аппаратные поворот/отражение → итоговый кадр 320×480
sensor.set_hmirror(True)
sensor.set_vflip(True)
sensor.set_transpose(True)

# Отключаем автоматику, чтобы цвета не плыли
sensor.set_auto_whitebal(False)
sensor.set_auto_gain(False)
sensor.skip_frames(time=2000)
clock = time.clock()

# ==================== ПАРАМЕТРЫ ЗЕРКАЛА ====================
CENTER_X     = 92    # X-координата центра на итоговом кадре 320×480
CENTER_Y     = 162    # Y-координата центра
RING_OUTER   = 170    # Внешний радиус рабочей зоны (пиксели)
RING_INNER   = 40     # Внутренний радиус рабочей зоны (пиксели)

# ==================== ЦВЕТОВЫЕ ПОРОГИ (LAB, НАСТРОЙТЕ ПОД СЕБЯ) ====================
THR_RED    = (30, 100, 15, 127, 15, 127)   # пример для красного
THR_YELLOW = (50, 100, -10, 10, 20, 127)   # пример для жёлтого
THR_BLUE   = (10, 60, -128, -20, -30, 30)   # пример для синего

# ==================== ФУНКЦИЯ ВЫЧИСЛЕНИЯ УГЛА ====================
def get_angle(x, y, cx, cy):
    """
    Угол в градусах [0..360). 0° – вверх по изображению (Y-), растёт по часовой стрелке.
    """
    dx = x - cx
    dy = y - cy
    angle = math.degrees(math.atan2(dx, -dy))
    return (angle + 360) % 360

# ==================== ОСНОВНОЙ ЦИКЛ ====================
print("Запуск... Смотрите в терминал OpenMV IDE")
while True:
    clock.tick()
    img = sensor.snapshot()

    # --- Маскирование: оставляем только кольцо ---
    img.mask_circle(CENTER_X, CENTER_Y, RING_OUTER, color=0)   # закрашивает всё снаружи
    img.draw_circle(CENTER_X, CENTER_Y, RING_INNER, color=0, fill=True)  # закрашивает внутренний круг

    # --- Отладочная графика (рисуем после маскирования, чтобы контуры были видны) ---
    img.draw_circle(CENTER_X, CENTER_Y, RING_OUTER, color=(0, 255, 0))  # внешняя граница зелёным
    img.draw_circle(CENTER_X, CENTER_Y, RING_INNER, color=(0, 255, 0))  # внутренняя граница зелёным
    img.draw_cross(CENTER_X, CENTER_Y, size=10, color=(255,255,255))    # центр
    img.draw_line(CENTER_X, CENTER_Y, CENTER_X, CENTER_Y - 30, color=(0,255,0))  # луч 0°

    # --- Поиск трёх цветных меток за один проход ---
    blobs = img.find_blobs([THR_RED, THR_YELLOW, THR_BLUE],
                           pixels_threshold=20, area_threshold=20, merge=True)

    # Разделяем блобы по коду цвета: code 1 – красный, 2 – жёлтый, 4 – синий
    red_blobs    = [b for b in blobs if b.code() == 1]
    yellow_blobs = [b for b in blobs if b.code() == 2]
    blue_blobs   = [b for b in blobs if b.code() == 4]

    # Выбираем крупнейший блоб каждого цвета (если он есть)
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
            # Подписываем угол на кадре
            img.draw_string(x, y, str(ang), color=(255,255,255))
        else:
            angles.append(-1)

    # --- Вывод в консоль ---
    fps = clock.fps()
    print(f"R:{angles[0]:>3} Y:{angles[1]:>3} B:{angles[2]:>3} | FPS:{fps}")
