## The modules we need ##

import struct
import serial
import time
from gDriveAPI import *
from mongoDB import *
from structData import *
from logBot import *

## The logging Part ##

setup_logging('./logConfig.json',logging.DEBUG,'LOG_CFG')
logger = logging.getLogger()

## The Connections Objects! The real importants things in the IoT ##

gLog = gDriveAPI('log','tag_system') #open the worksheet 'log' on the file 'tag_system'
gSes = gDriveAPI('open_session','tag_system')
gUser = gDriveAPI('soci','tag_system')

dbLog = mongoDB('radio_log','techlab') #work with the collection 'radio-logs' with the database 'techlab-db'

ser = serial.Serial('/dev/ttyAMA0',115200) #open a serial connection to talk with the gateway

## The laser session chronicle ##
id_session = int(gSes.read_one(1,1))

try:

    ser.write('i'+'2'+'\0')
    time.sleep(1)
    ser.write('j'+'\x00'+'\x00'+'\xc7'+'B'+'0'+'\0')

    # while True:
    #     pl = ser.readline()
    #     if len(pl) > 5:
    #         a_msg = radioPkt(pl)
    #         dbLog.write(a_msg.__dict__)
    #
    #
    #
    #         ### ################### ###
    #         ### Messagge from LASER ###
    #         ### ################### ###
    #         if a_msg.idm == 'n':
    #             logger.debug("n - mando crediti")
    #             cellTag = gUser.find(a_msg.tag[0:8])
    #             an_ans = answer(pl,gUser.read_one(cellTag.row, 3),gUser.read_one(cellTag.row, 4))
    #             logger.debug(an_ans.__dict__)
    #
    #             ser.write('i'+an_ans.idr+'\0')
    #             time.sleep(1)
    #             ser.write('j'+'\x00'+'\x00'+'\xc7'+'B'+an_ans.sk+'\0')
    #
    #             dbLog.write(an_ans.__dict__)
    #             logger.debug("mandato in db")
    #
    #             logger.debug("n - apro sessione")
    #             id_session = id_session + 1
    #             gSes.write(id_session+1,1,id_session) #id
    #             gSes.write(id_session+1,2,a_msg.date) #data
    #             gSes.write(id_session+1,4,gUser.read_one(cellTag.row, 8)) #mail
    #             gSes.write(id_session+1,5,0) #cr
    #
    #
    #
    #         ### ############################ ###
    #         ### Messagge from ENERGY MONITOR ###
    #         ### ############################ ###
    #         elif a_msg.idm == 'e':
    #             print "e"
    #             #plotly
    #
    #
    #
    #         ### ######################## ###
    #         ### Messagge from TICK LASER ###
    #         ### ######################## ###
    #         elif a_msg.idm == 't':
    #             print "t - aggiorno crediti"
    #             cr = float(gUser.read_one(cellTag.row, 3))
    #             sk = gUser.read_one(cellTag.row, 4)
    #             cr_new = cr - (0.2-(0.1*int(sk)))
    #             an_ans = answer(pl,cr_new,sk)
    #             logger.debug(an_ans.__dict__)
    #             gUser.write(cellTag.row, 3, cr_new)
    #
    #             print "t - mando a laser crediti"
    #             ser.write('i'+an_ans.idr+'\0')
    #             time.sleep(1)
    #             ser.write('j'+struct.pack('<f', float(an_ans.cr))+an_ans.sk+'\0')
    #
    #             print "t - aggiorno sessione"
    #
    #             gSes.write(id_session+1,4,float(gSes.read_one(id_session+1,4))+(0.2-(0.1*int(sk))))
    #             dbLog.write(an_ans.__dict__)
    #             logger.debug(an_ans.__dict__)
    #
    #
    #         else:
    #             print "altro"

except Exception, e:
    logging.error(e, exc_info=True)
    dbLog.close()
    ser.close()
