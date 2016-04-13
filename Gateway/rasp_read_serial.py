import serial

port = serial.Serial()
port.baudrate = 115200
port.port = '/dev/ttyAMA0'
port.open()
port.write(b'hello')
