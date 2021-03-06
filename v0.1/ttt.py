import struct
import serial


class radioPkt(object):
    def __init__(self, payload):
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

msg1 = '<,5977,4,1,-41,65,63,B9,8A,B9,42,>'
msg2 = '<,5969,2,1,-44,6E,3B,C2,72,62,33,81,>\r\n'

import logging
from logging.config import dictConfig

dictConfig(logging_config)

logger = logging.getLogger()

logger.debug('often makes a very good meal of %r', 'visiting tourists')
