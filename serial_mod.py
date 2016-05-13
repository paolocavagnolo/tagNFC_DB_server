import serial
import sys

def readline( to ):

    ser = serial.Serial('/dev/ttyAMA0',115200,timeout=to)
    line = ser.readline()
    ser.close()
    return line

def writeline( message ):

    ser = serial.Serial('/dev/ttyAMA0',115200,timeout=3)
    ser.write(message)
    ser.close()

def byte2float( data ):

    if (len(data[0])<2):
        data[0] = '0'+data[0]
    if (len(data[1])<2):
        data[1] = '0'+data[1]
    if (len(data[2])<2):
        data[2] = '0'+data[2]
    if (len(data[3])<2):
        data[3] = '0'+data[3]
    byte1 = ord(data[0].decode("HEX"))
    byte2 = ord(data[1].decode("HEX"))
    byte3 = ord(data[2].decode("HEX"))
    byte4 = ord(data[3].decode("HEX"))

    bytecc = [byte4, byte3, byte2, byte1]
    b = ''.join(chr(i) for i in bytecc)

    return float("{0:.2f}".format(struct.unpack('>f', b)[0]))
