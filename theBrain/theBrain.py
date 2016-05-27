## The modules we need ##

import serial
import time
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

ser = serial.Serial('/dev/ttyAMA0',115200) #open a serial connection to talk with the gateway

## The session chronicle ##
id_session = gSes.read_one(1,1)

try:
    while True:
        pl = ser.readline()
        if len(pl) > 5:
            a_msg = radioPkt(pl)
            dbLog.write(a_msg.__dict__)

            if a_msg.idm == 'n':
                print "n - mando crediti"
                cellTag = gUser.find(a_msg.tag[0:8])
                an_ans = answer(pl,gUser.read_one(cellTag.row, 3),gUser.read_one(cellTag.row, 4))
                dbLog.write(an_ans.__dict__)

                ser.write('i'+an_ans.idr+'\0')
                time.sleep(1)
                ser.write('j'+an_ans.cr_b+an_ans.sk+'\0')

                print "n - apro sessione"
                id_session = id_session + 1
                gSes.write(id_session+1,1,id_session) #id
                gSes.write(id_session+1,2,a_msg.date) #data
                gSes.write(id_session+1,4,gUser.read_one(cellTag.row, 8)) #mail
                gSes.write(id_session+1,5,0) #cr

            elif a_msg.idm == 'e':
                print "e"
                #plotly

            elif a_msg.idm == 't':
                print "t - aggiorno crediti"
                cr = gUser.read_one(cellTag.row, 3)
                sk = gUser.read_one(cellTag.row, 4)
                cr_new = cr - (0.2-(0.1*int(sk)))
                an_ans = answer(pl,cr_new,sk)
                dbLog.write(an_ans.__dict__)

                gUser.write(cellTag.row, 3, cr_new)

                print "t - mando a laser crediti"
                ser.write('i'+an_ans.idr+'\0')
                time.sleep(1)
                ser.write('j'+an_ans.cr_b+an_ans.sk+'\0')

                print "t - aggiorno sessione"

                gSes.write(id_session+1,4,gSes.read(id_session+1,4)+(0.2-(0.1*int(sk))))


            else:
                print "altro"

except:
    dbLog.close()
    dbEnergy.close()
    ser.close()
