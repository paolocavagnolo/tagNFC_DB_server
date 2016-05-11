import serial
from sys import argv

script, filename = argv

ser = serial.Serial('/dev/ttyAMA0',115200,timeout=1)
    
while True:
    try:
        if (ser.inWaiting() > 0):
            linea = ser.readline()
            open(filename,'a+').write(linea)
    except (KeyboardInterrupt, SystemExit):
        ser.close()
        buff.close()
        print "good close"
