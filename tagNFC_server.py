import serial

ser = serial.Serial('/dev/ttyAMA0',115200,timeout=1)

while True:
    linea = ser.readline()
    if (linea != ""):
        print linea.split("[")
