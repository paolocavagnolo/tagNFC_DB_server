import struct
import datetime

class radioPkt(object):
    def __init__(self, payload):
        self.payload_in = payload
        self.abs = payload.split(',')[1]
        self.ids = payload.split(',')[2]
        self.idr = payload.split(',')[3]
        self.RSSI = payload.split(',')[4]
        self.idm = payload.split(',')[5].decode("HEX")
        self.date = datetime.datetime.now()

        if self.idm == 'n':
            self.tag = ''.join(payload.split(',')[6:12])

        elif self.idm == 'e':
            self.idphase = payload.split(',')[6].decode("HEX")
            self.count = bytes2float(payload.split(',')[7:11])

class answer(radioPkt):
    def __init__(self, payload, cr, sk):
        super(answer, self).__init__(payload)
        self.idr = self.ids
        self.ids = 1
        self.date = datetime.datetime.now()
        if self.idm == 'n':
            self.cr = cr
            self.cr_b = list(float2bytes(float(cr)))
            # self.cr_unicode = unicode(float2bytes(float(cr)),errors = 'replace')
            self.sk = sk
        if self.idm == 't':
            self.cr = cr
            self.cr_b = list(float2bytes(float(cr)))
            # self.cr_unicode = unicode(float2bytes(float(cr)),errors = 'replace')
            self.sk = sk

        self.payload_out = '<i'+self.idr+'\0>'+' '+'<j'+self.cr_b+self.sk+'\0>'



class session(object):
    def __init__(self, msg):
        self.abs = payload.split(',')[1]
        self.ids = payload.split(',')[2]
        self.idr = payload.split(',')[3]
        self.RSSI = payload.split(',')[4]
        self.idm = payload.split(',')[5].decode("HEX")

        if self.idm == 'n':
            self.tag = ''.join(payload.split(',')[6:12])

        elif self.idm == 'e':
            self.idphase = payload.split(',')[6].decode("HEX")
            self.count = bytes2float(payload.split(',')[7:11])


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
    return struct.pack('<f', data)
