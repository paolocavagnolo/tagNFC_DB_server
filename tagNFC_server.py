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

import gspread
from oauth2client.service_account import ServiceAccountCredentials
scope = ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_name('/home/pi/Documents/techlab-tag-nfc-b3f2a2929d98.json', scope)

from pymongo import MongoClient

# read from gdrive
def db_pull(tag):
    try:
        return cellTag = worksheet.find(tag)
        print "found"
    except:
        print "not found"

# sync completely the db with gdrive
def db_sync(s_worksheet):
    s_client = MongoClient('mongodb://localhost:27017/')
    s_db = client['techlab-db']

    values_list = worksheet.row_values(1)

    print values_list

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
        l_client = MongoClient('mongodb://localhost:27017/')
        l_db = client['techlab-db']
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
                message = ''.join(linea.split(",")[4:8]);

                radio_log = {
                    "time" : datetime.datetime.now(),
                    "abs" : int(linea.split(",")[1]),
                    "ids" : int(linea.split(",")[2]),
                    "idr" : int(linea.split(",")[3]),
                    "message" : message,
                    "RSSI" : int(linea.split(",")[10])
                }



                t = threading.Thread(target=db_pull, args=(message,))
                t.start()

                l_db.radio_logs.insert(radio_log)
                print "Successfully inserted document: %s" % radio_log


        except (KeyboardInterrupt, SystemExit):
            client.close()
            ser.close()
