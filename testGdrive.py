import gdrive_mod as gdrive
import time

while True:
    open('testGdrive.txt','a+').write(gdrive.find("Cavagnolo"))
    time.sleep(30)
