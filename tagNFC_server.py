import serial

ser = serial.Serial('/dev/ttyAMA0',115200,timeout=1)

while True:
    try:
        #take
        linea = ser.readline()
        if (linea[0] == '#'):
            uid = linea.split(",")[4].split(" ")[0].split("x")[1] + linea.split(",")[4].split(" ")[1].split("x")[1] + linea.split(",")[4].split(" ")[2].split("x")[1] + linea.split(",")[4].split(" ")[3].split("x")[1]
            print uid



    except (KeyboardInterrupt, SystemExit):
        ser.close()
