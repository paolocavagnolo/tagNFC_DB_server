import serial

ser = serial.Serial('/dev/ttyAMA0',115200,timeout=3)

while True:
    if (ser.readLines() != ""):
        print ser.readLines()
