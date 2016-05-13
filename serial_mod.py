import serial
import sys

ser = serial.Serial('/dev/ttyAMA0',115200,timeout=1)

def readline():
    line = ser.readline()
    return line

def writeline( message ):
    ser.write(message)

def close()
    ser.close()
