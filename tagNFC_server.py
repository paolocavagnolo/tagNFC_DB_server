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

from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')
db = client['techlab-db']
soci_collection = db['soci']
log_collection = db['log']

from datetime import datetime
from pymongo import Connection
from pymongo.errors import ConnectionFailure

def main():
    try:
        ser = serial.Serial('/dev/ttyAMA0',115200,timeout=1)
    except ConnectionFailure, e:
        sys.stderr.write("Could not use serial: %s" % e)
        sys.exit(1)

    try:
        c = Connection(host="localhost", port=27017)
    except ConnectionFailure, e:
        sys.stderr.write("Could not connect to MongoDB: %s" % e)
        sys.exit(1)
    dbh = c['techlab']
    assert dbh.connection == c

    while True:
        try:
            if (ser.inWaiting() > 0):
                linea = ser.readLine()

                radio_log = {
                    "time" : datetime.datetime.now(),
                    "abs" : linea.split(",")[1],
                    "ids" : linea.split(",")[2],
                    "idr" : linea.split(",")[3],
                    "type" : linea.split(",")[4],
                    "message" : linea.split(",")[5:12],
                    "RSSI" : linea.split(",")[13]
                }

                dbh.radio_logs.insert(radio_log, safe=True)
                print "Successfully inserted document: %s" % radio_log
        except (KeyboardInterrupt, SystemExit):
            ser.close()

if __name__ == "__main__":
    main()
