#!/usr/bin/python


import gdrive_mod as excel
import mongodb_mod as db
import serial_mod as ser
#import plotly_mod as plot
import datetime
import struct

ser.close()
db.close()

"""
while True:
    try:
        #read from gateway
        if (ser.inWaiting() > 0):
            linea = ser.readline()
            print linea
            #read delivery data
            abss = int(linea.split(",")[1])
            ids = int(linea.split(",")[2])
            idr = int(linea.split(",")[3])
            time = datetime.datetime.now().time()
            message[0] = linea.split(",")[4]
            message[1] = linea.split(",")[5]
            message[2] = linea.split(",")[6]
            if (len(message[2])<2):
                message[2] = '0'+message[2]
            message[3] = linea.split(",")[7]
            if (len(message[3])<2):
                message[3] = '0'+message[3]
            message[4] = linea.split(",")[8]
            if (len(message[4])<2):
                message[4] = '0'+message[4]
            message[5] = linea.split(",")[9]
            if (len(message[5])<2):
                message[5] = '0'+message[5]
            RSSI = int(linea.split(",")[10])
            print ids
            #recode
            if (ids == 4):
                energyAmount = byte2float( message )
                radio_log = {
                    "time" : time,
                    "abs" : abss,
                    "ids" : ids,
                    "idr" : idr,
                    "idm" : message[0].decode("HEX"),
                    "idfase": message[1].decode("HEX"),
                    "enAmount": energyAmount,
                    "RSSI" : RSSI
                }
            #put line in db
            #db.radio_logs.insert(radio_log)
            print "Successfully inserted document: %s" % radio_log

    except (KeyboardInterrupt, SystemExit):
        client.close()
        ser.close()
        print "good close"
"""
