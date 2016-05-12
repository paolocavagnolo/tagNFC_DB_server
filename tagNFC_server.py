#!/usr/bin/python


import gdrive_mod as excel
import mongodb_mod as db
import serial_mod as ser
#import plotly_mod as plot
import datetime
import struct

# print "#"*20
#
# print "test gdrive"
# print "Trovi dei Cavagnolo? %r" % excel.find("Cavagnolo")
# print "Cosa c\'e\' in 5,2? %r" % excel.read(3,2)
# print "Scrivi qualcosa in 3,3? %r" % excel.write(3,3,52)
#
# print "#"*20
#
# print "test mongodb"
# print "Trovi dei 2? quanti? %r cosa? %r" % db.read({"ids": 4})
# print "Aggiungi un documento semplice semplice? %r" % db.write({"nome": "paolo", "cognome": "cavagnolo"})
#
# print "#"*20
#
# print "test serial"
# print "qualcosa in seriale? %r" % ser.readline()

try:
    while True:
        decision = raw_input('> ')
        if decision.split(' ')[0] == 'd':
            #open door
            ser.writeline("ciao")
            print "scritto"
        elif decision.split(' ')[1] == 'r':
            #read one line from serial and print it
            print ser.readline(decision.split(' ')[2])
        else:
            #ammazzati
            print "ammazzati"

except EOFError:
    db.close()
    print "\nBye"
