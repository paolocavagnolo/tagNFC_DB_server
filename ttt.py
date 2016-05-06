import struct

data = [65, 203, 96, 66, 11]
b = ''.join(chr(i) for i in data)

print struct.unpack('>f', b[0:4][::-1])
