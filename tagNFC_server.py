#!/usr/bin/python

import gdrive_mod as excel
import mongodb_mod as db
import serial_mod as ser
#import plotly_mod as plot
import datetime
import struct

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
        self.count = bytes2float(payload.split(',')[7:11])

class Laser_m(Delivery_info):
    def __init__(self, payload):
        self.tag = payload.split(',')[6:12]



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



try:
    while True:

        pl = ser.readline()
        if len(pl) > 5:
            print "1: read from serial: %r" % pl
            incoming = Delivery_info(pl)
            print "2: dictionary format: %r" % incoming.__dict__
            if incoming.__dict__['idm'] == 'n':
                #Tag NFC
                message = Laser_m(pl)
                print "3: retrieve important info: %r" % message.__dict__
                db.write(dict(incoming.__dict__.items() + message.__dict__.items()))
                print "4: wrote to mongodb: %r" % dict(incoming.__dict__.items() + message.__dict__.items())
                try:
                    print "5: finding this tag in gdrive: %r" % ''.join(message.__dict__['tag'][:4])
                    cellTag = excel.find(''.join(message.__dict__['tag'][:4]))
                except:
                    print "6: no one"
                    ser.writeline('i'+incoming.__dict__['ids'])
                    ser.writeline('o')
                else:
                    user = excel.read_row(cellTag.row)
                    #0: id      #4: Data rich   #8: Nome        #12: Residenza  #16: Quota 2016
                    #1: tagID   #5: Data acc    #9: Cognome     #13: CF         #17: Data annullamento
                    #2: Cr      #6: (tutore)    #10: Data Nas   #14: Qualifica
                    #3: Sk      #7: Mail        #11: Luogo      #15: Quota 2015
                    print "6: user: %r" % user
                    print "7: Credits: %r" % float(user[2])
                    print "8: Skill: %r" % user[3]
                    ser.writeline('i'+incoming.__dict__['ids'])
                    ser.writeline('j'+float2bytes(float(user[2]))+user[3])
                    print "9: %r" % ('c'+float2bytes(float(user[2]))+user[3])


            elif incoming.__dict__['idm'] == 'e':
                #Energy Tick
                message = Energy_m(pl)
                db.write(dict(incoming.__dict__.items() + message.__dict__.items()))
                print "wrote energy tic on db"

            elif incoming.__dict__['idm'] == 't':
                #Laser Tick
                print "tick"

            else:
                #ciao
                print "no recog"

        else:
            print "0: null"


except KeyboardInterrupt:
    db.close()
    ser.close()

    print "\nBye"
