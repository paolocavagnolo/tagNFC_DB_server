#!/usr/bin/python

import gdrive_mod as excel
import mongodb_mod as db
#import plotly_mod as plot
import datetime
import struct
import serial
import sys
import time
from apscheduler.schedulers.background import BackgroundScheduler

ser = serial.Serial('/dev/ttyAMA0',115200)

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
        self.tag = ''.join(payload.split(',')[6:12])


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

def db2drive_log():
    titoli = excel.read_row_log(1)
    records = db.read_last_N(10)
    l = 2
    for document in records:
        excel.update_linea(l, document)
        l = l + 1



scheduler = BackgroundScheduler()
#reopen_gdrive = scheduler.add_job(excel.open, 'interval', minutes=50)
#sync_db_gdrive_log = scheduler.add_job(db2drive_log, 'interval', minutes=30)
#scheduler.start()

#'a': ok        #'e': energy tick   #'i': node id       #'m': debug msg         #'q':           #'u':           #'y':
#'b':           #'f':               #'j': serial msg    #'n': NFC id            #'r':           #'v':           #'z':
#'c': credit    #'g':               #'k': test          #'o': no one            #'s':           #'w':
#'d':           #'h':               #'l': laser tick    #'p': 3d print tick     #'t': timeout   #'x':

#0: id      #4: Data rich   #8: Nome        #12: Residenza  #16: Quota 2016
#1: tagID   #5: Data acc    #9: Cognome     #13: CF         #17: Data annullamento
#2: Cr      #6: (tutore)    #10: Data Nas   #14: Qualifica
#3: Sk      #7: Mail        #11: Luogo      #15: Quota 2015

try:
    while True:
        print "waiting for serial bytes"
        pl = ser.readline()
        if len(pl) > 5:
            print "recieved %r" % (pl)
            now = datetime.datetime.now()
            incoming = Delivery_info(pl)

            if incoming.__dict__['idm'] == 'n':
                print "laser: %r" % (incoming.__dict__)
                #Tag NFC
                message = Laser_m(pl)
                db.write(dict(incoming.__dict__.items() + message.__dict__.items() + [('time',now)]))
                print "wrote on db: %r" % dict(incoming.__dict__.items() + message.__dict__.items() + [('time',now)])
                try:
                    print "search for user with that tag: %r" % message.__dict__['tag'][:8]
                    cellTag = excel.find(message.__dict__['tag'][:8])

                except:
                    #no one
                    print "no one"
                    ser.write('i'+incoming.__dict__['ids']+'\0')
                    time.sleep(1)
                    ser.write('j'+float2bytes(float('-1.1'))+'0'+'\0')

                    now = datetime.datetime.now()
                    db.write({'time':now, 'ids':1, 'idr':2, 'idm':'c', 'Cr':-1.1, 'Sk':0})
                    print "wrote on db: %r" % {'time':now, 'ids':1, 'idr':2, 'idm':'c', 'Cr':-1.1, 'Sk':0}

                else:
                    #fine someone!
                    print "find someone!"
                    user = excel.read_row(cellTag.row)

                    ser.write('i'+incoming.__dict__['ids']+'\0')
                    time.sleep(1)
                    ser.write('j'+float2bytes(float(user[2]))+user[3]+'\0')

                    now = datetime.datetime.now()
                    db.write({'time':now, 'ids':1, 'idr':2, 'idm':'c', 'Cr':float(user[2]), 'Sk':user[3]})
                    print "wrote on db: %r" % {'time':now, 'ids':1, 'idr':2, 'idm':'c', 'Cr':float(user[2]), 'Sk':user[3]}

            elif incoming.__dict__['idm'] == 'e':
                #Energy Tick
                print "energy tick"
                message = Energy_m(pl)
                db.write(dict(incoming.__dict__.items() + message.__dict__.items() + [('time',now)]))
                print "wrote on db: %r" % dict(incoming.__dict__.items() + message.__dict__.items() + [('time',now)])

            elif incoming.__dict__['idm'] == 't':
                #Laser Tick

            else:
                #ciao
                print "cose strane"

        else:
            print "waiting for serial bytes"

except KeyboardInterrupt:
    db.close()
    ser.close()

    print "\nBye"
