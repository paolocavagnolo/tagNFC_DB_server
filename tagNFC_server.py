#!/usr/bin/python

import gdrive_mod as excel
import mongodb_mod as db
import serial_mod as ser
#import plotly_mod as plot
import datetime
import struct

"""<,198,4,1,-40,65,62,FC,89,FB,42,>"""
class Delivery_info(object):

    def __init__(self, payload):
        self.abs = payload.split(',')[1]
        self.ids = payload.split(',')[2]
        self.idr = payload.split(',')[3]
        self.RSSI = payload.split(',')[4]
        self.idm = payload.split(',')[5].decode("HEX")

class Energy_m(Delivery_info):

    def __init__(self, payload):
        self.idphase = payload.split(',')[6].decode("HEX")
        self.count = byte2float(payload.split(',')[7:11])

class Laser_m(Delivery_info):

    def __init__(self, payload):
        self.tag = payload.split(',')[7:13]


def byte2float( data ):

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



try:
    while True:

        pl = ser.readline(1)
        if len(pl) > 2:
            del_info = Delivery_info(pl)

            if del_info.__dict__['idm'] == 'n':
                #Tag NFC
                message = Laser_m(pl)
                print dict(del_info.__dict__.items() + message.__dict__.items())

            elif del_info.__dict__['idm'] == 'e':
                #Energy Tick
                message = Energy_m(pl)
                print dict(del_info.__dict__.items() + message.__dict__.items())

            elif del_info.__dict__['idm'] == 't':
                #ciao

            else:
                print "no recog"


except KeyboardInterrupt:
    db.close()
    print "\nBye"
