## The modules we need ##

import serial
from gDriveAPI import *
from mongoDB import *
from structData import *

## The logging Part ##

# FORMAT = '%(asctime)-15s %(clientip)s %(user)-8s %(message)s'
# logging.basicConfig(format=FORMAT)
# d = {'clientip': '192.168.0.1', 'user': 'fbloggs'}
# logger = logging.getLogger('tcpserver')
# logger.warning('Protocol problem: %s', 'connection reset', extra=d)

## The Connections Objects! The real importants things in the IoT ##

gLog = gDriveAPI('log','tag_system') #open the worksheet 'log' on the file 'tag_system'
gSes = gDriveAPI('open_session','tag_system')
gUser = gDriveAPI('soci','tag_system')

dbLog = mongoDB('radio_log','techlab') #work with the collection 'radio-logs' with the database 'techlab-db'
dbEnergy = mongoDB('energy','techlab')

ser = serial.Serial('/dev/ttyAMA0',115200) #open a serial connection to talk with the gateway


try:
    while True:
        pl = ser.readline()
        if len(pl) > 5:
            a_msg = radioPkt(pl)
            if a_msg.idm == 'n':
                print "n"
                print gUser.read_one(gUser.find(a_msg.tag).row, 3)

            elif a_msg.idm == 'e':
                print "e"
                

            elif a_msg.idm == 'l':
                print "l"

            else:
                print "altro"

except:
    dbLog.close()
    dbEnergy.close()
    ser.close()
