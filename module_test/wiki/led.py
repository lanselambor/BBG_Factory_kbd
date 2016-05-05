import mraa, time

led = mraa.Gpio(60)
led.dir(mraa.DIR_OUT)
status = 1

while True:
    led.write(status)
    status = status ^ 1
    time.sleep(1)
