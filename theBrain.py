
## The Connections Objects! The real importants things in the IoT ##

gLog = gDriveAPI('log','tag_system') #open the worksheet 'log' on the file 'tag_system'
gSes = gDriveAPI('session','tag_system')
gUser = gDriveAPI('soci','tag_system')

dbLog = mongoDB('radio_logs','techlab-db') #work with the collection 'radio-logs' with the database 'techlab-db'
dbEnergy = mongoDB('energy','techlab-db')

ser = serial.Serial('/dev/ttyAMA0',115200) #open a serial connection to talk with the gateway


## The information driver! The cool stuff. ##

a_msg = radioPkt(payload)



try:
    while True:
        #Read serial





except KeyboardInterrupt:
    db.close()
    ser.close()
    print "\nBye"
