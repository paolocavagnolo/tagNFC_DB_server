## The modules we need ##

from gDriveAPI import *
from mongoDB import *
from strucData import *

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

## The information driver! The cool stuff. ##

msg1 = '<,5977,4,1,-41,65,63,B9,8A,B9,42,>'
msg2 = '<,5969,2,1,-44,6E,3B,C2,72,62,33,81,>\r\n'

a_msg = radioPkt(msg1)

print a_msg.__dict__

dbLog.close()
dbEnergy.close()
ser.close()
