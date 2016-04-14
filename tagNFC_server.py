import serial

#serial part
ser = serial.Serial('/dev/ttyAMA0',115200,timeout=1)

#node js part
from Naked.toolshed.shell import execute_js, muterun_js


while True:
    try:
        #read from serial
        x = ser.read()

        #select lines
        if (x == '#'):
            linea = ser.readline()
            uid = linea.split(",")[4].split(" ")[0].split("x")[1] + linea.split(",")[4].split(" ")[1].split("x")[1] + linea.split(",")[4].split(" ")[2].split("x")[1] + linea.split(",")[4].split(" ")[3].split("x")[1]
            cc = 1
            print uid

        if (cc == 1):
            muterun_js('/home/pi/Database/read_gsheet.js 2 3')
            cc = 0;

    except (KeyboardInterrupt, SystemExit):
        ser.close()
