import serial
from sys import argv

script, filename = argv

ser = serial.Serial('/dev/ttyAMA0',115200,timeout=1)

buff = open(filename,'a+')

while True:
    if (ser.inWaiting() > 0):
        linea = ser.readline()
        buff.write(linea)
