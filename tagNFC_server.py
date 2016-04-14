import serial

ser = serial.Serial('/dev/ttyAMA0',115200,timeout=1)

while True:
    try:
        linea = ser.readline()
        if (linea != ""):
            for item in linea.split(",")[4].split(" "):
                print item.split("x").[1]

    except (KeyboardInterrupt, SystemExit):
        ser.close()
