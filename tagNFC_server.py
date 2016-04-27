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
gc = gspread.authorize(credentials)
sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1KWxCi7tny8uxo4TmzjNnVuNj5eGRVngwFD2gxIX5qfw/edit?usp=sharing')
worksheet = sh.worksheet("soci")

from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')
db = client['techlab-db']

# t = threading.Thread(target=sync_db)
# threads.append(t)
#
#
# def sync_db():




def main():
    try:
        ser = serial.Serial('/dev/ttyAMA0',115200,timeout=1)
    except ConnectionFailure, e:
        sys.stderr.write("Could not use serial: %s" % e)
        sys.exit(1)

    while True:
        try:
            if (ser.inWaiting() > 0):
                linea = ser.readline()
                message = ''.join(linea.split(",")[4:10]);

                radio_log = {
                    "time" : datetime.datetime.now(),
                    "abs" : int(linea.split(",")[1]),
                    "ids" : int(linea.split(",")[2]),
                    "idr" : int(linea.split(",")[3]),
                    "message" : message,
                    "RSSI" : int(linea.split(",")[10])
                }

                cellTag = worksheet.find(message)

                db.radio_logs.insert(radio_log)
                print "Successfully inserted document: %s" % radio_log



        except (KeyboardInterrupt, SystemExit):
            client.close()
            ser.close()

if __name__ == "__main__":
    main()
