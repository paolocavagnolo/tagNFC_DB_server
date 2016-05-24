## The modules we need ##

from gDriveAPI import *


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
#
# dbLog = mongoDB('radio_logs','techlab-db') #work with the collection 'radio-logs' with the database 'techlab-db'
# dbEnergy = mongoDB('energy','techlab-db')
#
# ser = serial.Serial('/dev/ttyAMA0',115200) #open a serial connection to talk with the gateway
#
# ## The information driver! The cool stuff. ##
#
# a_msg = radioPkt(payload)

print gLog.find('2')
print gSes.find('5')
print gUser.find('Paolo ')
print gLog.find('2')
print gSes.find('5')
print gUser.find('Paolo ')
