#import gdrive_mod as gdrive
import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import gdrive_mod as gdrive

scheduler = BackgroundScheduler()


now = datetime.datetime.now()


def open_gdrive():
    print "ciao_fun"

#
# while True:
#     gdrive.open(
#     open('testGdrive.txt','a+').write(gdrive.read_one(5,6)+' '+(time.strftime("%H:%M:%S"))+'\n')
#     time.sleep(30)
job = scheduler.add_job(gdrive.open, 'interval', minutes=1)

scheduler.start()


while True:
    gdrive.open()
    open('testGdrivex.txt','a+').write(gdrive.read_one(5,5)+' '+now.strftime("%Y-%m-%d %H:%M"))
