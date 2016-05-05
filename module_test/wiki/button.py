import mraa, time

button = mraa.Gpio(62)
button.dir(mraa.DIR_IN)

while True:
    print button.read()
    time.sleep(.5)
