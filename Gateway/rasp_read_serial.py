import serial

port = serial.Serial("/dev/ttyAMA0", baudrate=115200, timeout=3.0)

while True:
    if port.available():
        print "ciao"
