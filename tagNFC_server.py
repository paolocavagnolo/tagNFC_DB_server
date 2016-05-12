#!/usr/bin/python


import gdrive_mod as excel
import mongodb_mod as db
import serial_mod as ser
#import plotly_mod as plot
import datetime
import struct


print "Trovi dei Cavagnolo? %r" % excel.find("Cavagnolo")
print "Cosa c\'e\' in 3,2? %r" % excel.read(3,2)
print "Scrivi qualcosa in 3,3? %r" % excel.write(3,3,52)


ser.close()
db.close()
