#!/usr/bin/python


import gdrive_mod as excel
import mongodb_mod as db
import serial_mod as ser
#import plotly_mod as plot
import datetime
import struct

class Energy_m(object):

    def __init__(self, payload):
        self.abs = payload.split(',')[1]
        self.ids = payload.split(',')[2]
        self.idr = payload.split(',')[3]
        self.idm = payload.split(',')[4]
        self.RSSI = payload.split(',')[5]
        self.idphase = payload.split(',')[6]
        self.count = byte2float(payload.split(',')[7:11])


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
        decision = raw_input('> ')
        lenDecision = len(decision.split(' '))
        primo = decision.split(' ')[0]

        if primo == 'd':
            #open door
            ser.writeline("ciao")
            print "scritto"

        elif primo == 'r' and lenDecision > 1:
            #read one line from serial and put it in the db print it
            pl = ser.readline(int(decision.split(' ')[1]))
            print pl
            message = Energy_m(pl)
            print message


        else:
            #ammazzati
            print "ammazzati"

except EOFError:
    db.close()
    print "\nBye"
