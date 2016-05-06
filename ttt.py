import struct

data = [65, 203, 96, 66]
b = ''.join(chr(i) for i in data)

print struct.unpack('>f', b[4:0])
