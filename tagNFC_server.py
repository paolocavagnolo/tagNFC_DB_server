# Thread1:
# Leggo seriale
# Scrivo MongoDB
# Leggo MongoDB
# Scrivo seriale
#
#
# Thread2:
# Leggo gsheet
# Scrivo MongoDB
# Leggo MongoDB
# Scrivo serial

#!/usr/bin/python

import serial
import pymongo
import datetime
import threading
import struct

import gspread
from oauth2client.service_account import ServiceAccountCredentials
scope = ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_name('/home/pi/Documents/techlab-tag-nfc-b3f2a2929d98.json', scope)

from pymongo import MongoClient

# # read from gdrive
# def db_pull(tag):
#     try:
#         values_list = worksheet.row_values(1)
#         print "found"
#     except:
#         print "not found"
#
# # sync completely the db with gdrive
# def db_sync(s_worksheet):
#
#
#     print values_list

# write on gdrive


while True:
    # Gspread!
    try:
        gc = gspread.authorize(credentials)
        sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1KWxCi7tny8uxo4TmzjNnVuNj5eGRVngwFD2gxIX5qfw/edit?usp=sharing')
        worksheet = sh.worksheet("soci")
    except:
        print "problem with gspread"

    # MongoDB!
    try:
        client = MongoClient('mongodb://localhost:27017/')
        db = client['techlab-db']
    except:
        print "problem with mongodb"

    # Serial!
    try:
        ser = serial.Serial('/dev/ttyAMA0',115200,timeout=1)
    except ConnectionFailure, e:
        sys.stderr.write("Could not use serial: %s" % e)
        sys.exit(1)

    # Go
    print "go"
    while True:
        try:
            if (ser.inWaiting() > 0):
                linea = ser.readline()
                message = ''.join(linea.split(",")[4:9]);

                radio_log = {
                    "time" : datetime.datetime.now(),
                    "abs" : int(linea.split(",")[1]),
                    "ids" : int(linea.split(",")[2]),
                    "idr" : int(linea.split(",")[3]),
                    "message" : message,
                    "RSSI" : int(linea.split(",")[10])
                }

                print struct.pack('4f',message[1:4])


                # t = threading.Thread(name="dbPull", target=db_pull, args=(message,))
                # t.start()
                db.radio_logs.insert(radio_log)
                print "Successfully inserted document: %s" % radio_log

                # if (ids == 2):
                #     if (message[6] == 'l'):
                #         # we are in the tick mother fucker
                #
                #
                #     else:
                #         # we are in the enable process
                #         cellTag = worksheet.find(message)
                #         ser.write(float(worksheet.cell(cellTag.row, 3).value))
                #         ser.write(int(worksheet.cell(cellTag.row, 4).value))
                #         print "valori mandati in seriale"



        except (KeyboardInterrupt, SystemExit):
            client.close()
            ser.close()
            print "good close"
