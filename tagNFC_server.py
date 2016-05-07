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

abss = 0
ids = 0
idr = 0
message = [0,1,2,3,4,5]
RSSI = 0
energyAmount = 0

def byte2float( bytess ):

    data = bytess
    byte1 = ord(data[2].decode("HEX"))
    byte2 = ord(data[3].decode("HEX"))
    byte3 = ord(data[4].decode("HEX"))
    byte4 = ord(data[5].decode("HEX"))

    bytecc = [byte4, byte3, byte2, byte1]
    b = ''.join(chr(i) for i in bytecc)

    return float("{0:.2f}".format(struct.unpack('>f', b)[0]))

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
                        "idm" : message[0],
                        "idfase": message[1],
                        "enAmount": energyAmount,
                        "RSSI" : RSSI
                    }
                #put line in db
                #db.radio_logs.insert(radio_log)
                print "Successfully inserted document: %s" % radio_log
                #do actions to internet



            #read from internet




        except (KeyboardInterrupt, SystemExit):
            client.close()
            ser.close()
            print "good close"
