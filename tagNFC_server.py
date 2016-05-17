#!/usr/bin/python

import gdrive_mod as excel
import mongodb_mod as db
#import plotly_mod as plot
import datetime
import struct
import serial
import sys
import time
import logging
from apscheduler.schedulers.background import BackgroundScheduler

ser = serial.Serial('/dev/ttyAMA0',115200)
logging.basicConfig()

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

class Session(object):
    def __init__(self, num, tempo, tagID, cr):
        self.id = num
        self.time = tempo
        self.tag = tagID
        self.cr = 0

    mail = ""



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
    print '#'*10
    print "DB2DRIVE_LOG!!!"
    print '#'*10
    titoli = excel.read_row_log(1)
    records = db.read_last_N(10)
    l = 2
    for document in records:
        excel.update_linea(l, document, titoli)
        l = l + 1

# def plotgo():
#     x = []
#
#     #prendi roba dal file
#     ff = open('buffer_plot.txt','a+')
#
#     for line in ff:
#         if line.split(',')[1] == '4'
#
#     #manda su plotly
#
#     #tronca il file
#     ff.truncate()
#     ff.close()

scheduler = BackgroundScheduler()
#reopen_gdrive = scheduler.add_job(excel.open, 'interval', minutes=2)
sync_db_gdrive_log = scheduler.add_job(db2drive_log, 'interval', minutes=5)
#data2plotly = scheduler.add_job(plotgo, 'interval', minutes=60)
scheduler.start()

#'a': ok        #'e': energy tick   #'i': node id       #'m': debug msg         #'q':           #'u':           #'y':
#'b':           #'f':               #'j': serial msg    #'n': NFC id            #'r':           #'v':           #'z':
#'c': credit    #'g':               #'k': test          #'o': no one            #'s':           #'w':
#'d':           #'h':               #'l': laser tick    #'p': 3d print tick     #'t': timeout   #'x':

#0: id      #4: Data rich   #8: Nome        #12: Residenza  #16: Quota 2016
#1: tagID   #5: Data acc    #9: Cognome     #13: CF         #17: Data annullamento
#2: Cr      #6: (tutore)    #10: Data Nas   #14: Qualifica
#3: Sk      #7: Mail        #11: Luogo      #15: Quota 2015

id_session = int(excel.read_session(1,1))

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

                id_session = id_session + 1
                laser_session = Session(id_session, now, message.__dict__['tag'],0)
                excel.write_session(id_session+1,1,id_session)
                excel.write_session(id_session+1,2,now)
                excel.write_session(id_session+1,3,laser_session.tag)

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
                    laser_session.mail = user[7]
                    excel.write_session(id_session+1,4,laser_session.mail)

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
                print "wrote on db_log: %r" % dict(incoming.__dict__.items() + message.__dict__.items() + [('time',now)])
                db.write_energy(dict(message.__dict__.items() + [('time',now)] + [('nodeID',4)]))
                open('buffer_plot.txt','a+').write(now.strftime('%Y/%m/%d %H:%M:%S') + ',' + '4' + ',' + message.__dict__['idphase'] + ',' + str(message.__dict__['count']) + '\n')

            elif incoming.__dict__['idm'] == 't':
                #Laser Tick
                print "laser tick"

                # update credit
                Cr_old = user[2]
                Cr_new = Cr_old-(0.2-(0.1*int(user[3])))

                laser_session.cr = laser_session.cr + (0.2-(0.1*int(user[3])))

                # write it on excel
                excel.write(cellTag.row, 2, Cr_new)

                # send the new credit on the laser display
                ser.write('i'+incoming.__dict__['ids']+'\0')
                time.sleep(1)
                ser.write('j'+float2bytes(float(Cr_new))+user[3]+'\0')

                # update the session
                excel.write_session(id_session+1,5,laser_session.cr)

                db.write(dict(incoming.__dict__.items() + [('time',now)]))





            else:
                #ciao
                print "cose strane"

        else:
            print "waiting for serial bytes"

except KeyboardInterrupt:
    db.close()
    ser.close()

    print "\nBye"
