from theBrain import *

# Check internet connection!
gUser = gDriveAPI('soci','tag_system')
gSes = gDriveAPI('open_session','tag_system')

dbLog = mongoDB('radio_log','techlab') #work with the collection 'radio-logs' with the database 'techlab-db'


state = 0
id_session = int(gSes.read_one(1,1))

## INPUT - state 0 >> 1##
if state == 0:
    RFmsg = ""
    if readFromSerial(RFmsg):   # Firs of all, look at the serial port for communication from moteino
        msgIn = radioPkt(RFmsg)
        state = 0
    elif readFromTelegram():    # Secondly, look at telegram
        msgIn = telegramPkt()
        state = 0
    else:
        print "no input"

## PROCESS
elif state == 1:
    dbLog.write(msg.__dict__)   ## msg to mongo online database

    if msg.idm == 'n':      ## NFC from laser
        msgOut = checkMember(msgIn, gUser)
        openSession(msgIn, id_session, gSes, gUser)
        state = 2

    elif msg.idm == 't':    ## Laser tick
        msgOut = updateMember(msgIn)
        state = 2

    elif msg.idm == 'e':    ## Energy tick
        updateEnergy(msgIn)
        state = 0

    elif msg.idm == 'b':
        msgOut = telegramPrs(msgIn)
        state = 2
        # elif msg.cmd == 'door':  ## Door
        #
        # elif msg.cmd == 'temp':  ## Get temperature
        #     s
        # elif msg.cmd == 'umidity': ## Get umidity
        #     s
        # elif msg.cmd == 'sound': ## Get sound
        #     s
        # elif msg.cmd == 'air': ## Get quality of the air

## OUTPUT
elif state == 2:
    dbLog.write(msgOut.__dict__)   ## msg to mongo online database
    goReal(msgOut)
