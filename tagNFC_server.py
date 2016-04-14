import serial
from pymongo import MongoClient

#serial part
ser = serial.Serial('/dev/ttyAMA0',115200,timeout=1)

#mongodb part
client = MongoClient('localhost', 27017)
db = client['techlab']
collection = db['soci']
cc = 0

while True:
    try:
        #read from serial
        x = ser.read()

        #select lines
        if (x == '#'):
            linea = ser.readline()
            uid = linea.split(",")[4].split(" ")[0].split("x")[1] + linea.split(",")[4].split(" ")[1].split("x")[1] + linea.split(",")[4].split(" ")[2].split("x")[1] + linea.split(",")[4].split(" ")[3].split("x")[1]
            cc = 1
            print uid

        #check into DB
        if (cc == 1):
            cursor = db.collection.find({"Nome": "Paolo"})
            print cursor
            cc = 0

    except (KeyboardInterrupt, SystemExit):
        ser.close()
