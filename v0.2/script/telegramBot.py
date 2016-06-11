import sys
import time
import telepot
import pprint

SYSTEM_PATH = '/home/pi/Documents/'
PATH_KEYS = SYSTEM_PATH + 'keys.txt'
fkey=open(PATH_KEYS,'r')
fkeylines=fkey.readlines()
TELEGRAM_BRIDGE = SYSTEM_PATH + fkeylines[5].split('\n')[0]
TELEGRAM_KEY = fkeylines[11].split('\n')[0]
fkey.close()

print TELEGRAM_KEY

def handle(msg):
    fbridge = open(TELEGRAM_BRIDGE, 'w')
    pprint.pprint(msg, fbridge)
    fbridge.close()


bot = telepot.Bot(TELEGRAM_KEY)
bot.message_loop(handle)
print ('Listening ...')

# Keep the program running.
while 1:
    time.sleep(10)
