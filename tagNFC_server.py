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

from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')
db = client['techlab-db']



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

                radio_log = {
                    "time" : datetime.datetime.now(),
                    "abs" : int(linea.split(",")[1]),
                    "ids" : int(linea.split(",")[2]),
                    "idr" : int(linea.split(",")[3]),
                    "message" : int.hex(linea.split(",")[4:10]),
                    "RSSI" : int(linea.split(",")[10])
                }

                db.radio_logs.insert(radio_log)
                print "Successfully inserted document: %s" % radio_log
        except (KeyboardInterrupt, SystemExit):
            ser.close()

if __name__ == "__main__":
    main()
