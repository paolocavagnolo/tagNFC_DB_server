import serial

port = serial.Serial()
port.baudrate = 115200
port.port = '/dev/ttyAMA0'
port.open()
print(port.is_open)
