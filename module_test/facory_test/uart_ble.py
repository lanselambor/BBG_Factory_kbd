import serial

ser = serial.Serial(port = "/dev/ttyO2", baudrate=9600)

ser.write("AT")
print ser.read(2)
