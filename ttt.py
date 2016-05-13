import struct

class Delivery_info(object):

    def __init__(self, payload):
        self.abs = payload.split(',')[1]
        self.ids = payload.split(',')[2]
        self.idr = payload.split(',')[3]
        self.idm = payload.split(',')[4]
        self.RSSI = payload.split(',')[5]

class Energy_m(Delivery_info):

    def __init__(self, payload):
        self.idphase = payload.split(',')[6]
        self.count = byte2float(payload.split(',')[7:11])

def bytes2float( data ):

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

def float2bytes( data ):
    byte = [0,0,0,0]
    up = struct.pack('<f', data)
    byte[0] = up[0].encode("HEX")
    byte[1] = up[1].encode("HEX")
    byte[2] = up[2].encode("HEX")
    byte[3] = up[3].encode("HEX")
    return byte

ex = ['e1', 'fa', '55', '43']

print bytes2float(ex)
print ex
print float2bytes(float(raw_input('f2b> ')))
