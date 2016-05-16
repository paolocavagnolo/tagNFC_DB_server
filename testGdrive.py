import gdrive_mod as gdrive
import time

while True:
    open('testGdrive.txt','a+').write(gdrive.read_one(5,6)+' '+(time.strftime("%H:%M:%S"))+'\n')
    time.sleep(30)
