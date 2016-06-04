import time
import datetime
import telepot

def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']

    print 'Got command: %s' % command

    if command == '/door':
        stringa = str(datetime.datetime.now()) + ',' + str(msg['from']['first_name']) + ' ' + str(msg['from']['last_name']) + ',' + str(command) + '\n'
        open('test.txt','a+').write(stringa)
        bot.sendMessage(chat_id,"ok!")


bot = telepot.Bot('223540260:AAE5dNuHTt5F9m3gGHNxieghQgP58EzxilU')

bot.message_loop(handle)
