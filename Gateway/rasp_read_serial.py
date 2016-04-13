import serial

serial.Serial() as ser:
    ser.baudrate = 115200
    ser.port = '/dev/ttyAMA0'
    ser.open()
    ser.write(b'hello')
