import serial

#link with moteino
moteino = serial.Serial()
moteino.baudrate = 115200
moteino.port = '/dev/ttyAMA0'
moteino.timeout = 3
moteino.open()
print(moteino)

if (moteino.readlines):
    print "ciao"
