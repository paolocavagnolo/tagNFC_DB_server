import struct

def byte2float( bytess ):

    data = bytess
    byte1 = ord(data[0:2].decode("HEX"))
    byte2 = ord(data[2:4].decode("HEX"))
    byte3 = ord(data[4:6].decode("HEX"))
    byte4 = ord(data[6:8].decode("HEX"))

    bytecc = [byte4, byte3, byte2, byte1]
    b = ''.join(chr(i) for i in bytecc)

    return struct.unpack('>f', b)[0]



cippo = "3DB54B42"
print byte2float(cippo)
