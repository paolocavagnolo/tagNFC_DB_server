import telepot

# def check_telegram(bot):
#     msg = bot.getUpdates(offset=100000001)
#
#     chat_id = msg['chat']['id']
#     command = msg['text']
#
#     print 'Got command: %s' % command
#
#     # if command == '/door' and chat_id == -123571607:
#     if command == '/door':
#         stringa = str(datetime.datetime.now()) + ',' + str(msg['from']['first_name']) + ' ' + str(msg['from']['last_name']) + ',' + str(command) + '\n'
#         open('/home/pi/Documents/tagNFC_DB_server/theBrain/test.txt','a+').write(stringa)
#         bot.sendMessage(chat_id,"ok!")


a_bot = telepot.Bot('223540260:AAE5dNuHTt5F9m3gGHNxieghQgP58EzxilU')
msg = a_bot.getUpdates(offset=100000001)
