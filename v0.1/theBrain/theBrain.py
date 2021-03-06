#!/usr/bin/env python

## The modules we need ##
import serial
import time
import os
import sys

from gDriveAPI import *
from mongoDB import *
from structData import *
from logBot import *


## The logging Part ##
ENERGYLOG = '/home/pi/Documents/tagNFC_DB_server/theBrain/energyBuffer.log'
setup_logging('/home/pi/Documents/tagNFC_DB_server/theBrain/logConfig.json',logging.DEBUG,'LOG_CFG')
logger = logging.getLogger()

## The Connections Objects! The real importants things in the IoT ##
wired = False

while wired == False:
    try:
        gLog = gDriveAPI('log','tag_system') #open the worksheet 'log' on the file 'tag_system'
        gSes = gDriveAPI('open_session','tag_system')
        gUser = gDriveAPI('soci','tag_system')
        wired = True
    except:
        time.sleep(10)

dbLog = mongoDB('radio_log','techlab') #work with the collection 'radio-logs' with the database 'techlab-db'


ser = serial.Serial('/dev/ttyAMA0',115200, timeout=3) #open a serial connection to talk with the gateway

## The laser session chronicle ##
id_session = int(gSes.read_one(1,1))


## Read from serial


try:
    while True:
        pl = ser.readline()
        if len(pl) > 2:
            if pl[0] == '<' and pl[1] == ',':
                logger.debug(pl)
                a_msg = radioPkt(pl)
                dbLog.write(a_msg.__dict__)

                ### ################### ###
                ### Messagge from LASER ###
                ### ################### ###
                if a_msg.idm == 'n':
                    logger.debug("n - mando crediti")
                    cellTag = gUser.find(a_msg.tag[0:8])
                    an_ans = answer(pl,gUser.read_one(cellTag.row, 3),gUser.read_one(cellTag.row, 4))
                    logger.debug(an_ans.__dict__)

                    ser.write('i'+an_ans.idr+'\0')
                    time.sleep(1)
                    ser.write('j'+an_ans.cr_b+an_ans.sk+'\0')

                    db_ans = an_ans.__dict__
                    db_ans.pop('cr_b',None)
                    dbLog.write(db_ans)
                    logger.debug("mandato in db")

                    logger.debug("n - apro sessione")
                    id_session = id_session + 1
                    gSes.write(id_session+1,1,id_session) #id
                    gSes.write(id_session+1,2,a_msg.date) #data
                    gSes.write(id_session+1,3,gUser.read_one(cellTag.row, 8)) #mail
                    gSes.write(id_session+1,4,0) #cr



                ### ############################ ###
                ### Messagge from ENERGY MONITOR ###
                ### ############################ ###
                elif a_msg.idm == 'e':
                    logger.debug("energy!")

                    #plotly
                    logger.debug(open(ENERGYLOG,'a+',0).write(str(a_msg.date) + ',' + str(a_msg.idphase) + ',' + str(a_msg.count) + '\n'))
                    logger.debug(os.system("plotData.sh"))


                ### ######################## ###
                ### Messagge from TICK LASER ###
                ### ######################## ###
                elif a_msg.idm == 't':
                    logger.debug("t - aggiorno crediti")
                    cr = float(gUser.read_one(cellTag.row, 3))
                    sk = gUser.read_one(cellTag.row, 4)
                    cr_new = cr - (0.2-(0.1*int(sk)))
                    an_ans = answer(pl,cr_new,sk)
                    logger.debug(an_ans.__dict__)
                    gUser.write(cellTag.row, 3, cr_new)

                    logger.debug("t - mando a laser crediti")
                    ser.write('i'+an_ans.idr+'\0')
                    time.sleep(1)
                    ser.write('j'+an_ans.cr_b+an_ans.sk+'\0')

                    logger.debug("t - aggiorno sessione")
                    gSes.write(id_session+1,4,float(gSes.read_one(id_session+1,4))+(0.2-(0.1*int(sk))))
                    db_ans = an_ans.__dict__
                    db_ans.pop('cr_b',None)
                    dbLog.write(db_ans)
                    logger.debug(db_ans)
                    logger.debug("mandato in db")


                else:
                    logger.debug("altro")

        ## if nothing arrived at serial:
        else:
            ##check if file exist
            if os.path.isfile('/home/pi/Documents/tagNFC_DB_server/theBrain/bridge2brain.txt'):
                ser.write('i'+'3'+'\0')
                time.sleep(1)
                ser.write('j'+'d'+'\0')
                logger.debug(os.system("rm /home/pi/Documents/tagNFC_DB_server/theBrain/bridge2brain.txt"))



except Exception, e:
    logging.error(e, exc_info=True)
    logger.info("CHIUSO!", exc_info=True)
    dbLog.close()
    ser.close()
