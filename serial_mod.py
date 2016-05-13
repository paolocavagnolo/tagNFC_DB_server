import serial
import sys



def readline():
    ser = serial.Serial('/dev/ttyAMA0',115200,timeout=1)
    line = ser.readline()
    ser.close()
    return line

def writeline( message ):
    ser = serial.Serial('/dev/ttyAMA0',115200,timeout=1)
    ser.write(message)
    ser.close()
