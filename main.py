import sensor, image, time
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.HVGA)
sensor.set_hmirror(True)
sensor.set_vflip(True)
sensor.set_transpose(True)
sensor.skip_frames(time=2000)
clock = time.clock()
while True:
    clock.tick()
    img = sensor.snapshot()
    print(clock.fps())
