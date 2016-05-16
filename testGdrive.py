#import gdrive_mod as gdrive
import time
import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import gdrive_mod as gdrive

scheduler = BackgroundScheduler()


now = datetime.datetime.now()

def gdrive_open():
    gdrive.open()
    print "renew!"

#
# while True:
#     gdrive.open(
#     open('testGdrive.txt','a+').write(gdrive.read_one(5,6)+' '+(time.strftime("%H:%M:%S"))+'\n')
#     time.sleep(30)
job = scheduler.add_job(gdrive_open, 'interval', seconds=30)

scheduler.start()


while True:
    open('testGdrivex.txt','a+').write(gdrive.read_one(5,5)+' '+now.strftime("%Y-%m-%d %H:%M")+'\n')
