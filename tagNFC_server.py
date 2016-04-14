import serial

ser = serial.Serial('/dev/ttyAMA0',115200,timeout=1)

while True:
    try:
        linea = ser.readline()
        if (linea != ""):
            print linea.split(",")[4].split("x")
    except (KeyboardInterrupt, SystemExit):
        ser.close()
