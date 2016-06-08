import telepot

## Start the telegram bot
old_date = 0

def check_telegram(bot):
    logger.debug("telegram")
    global old_date
    msg = bot.getUpdates(offset=100000001)

    chat_id = msg[len(msg)-1]['message']['chat']['id']
    command = msg[len(msg)-1]['message']['text']
    date = msg[len(msg)-1]['message']['date']
    print 'Got command: %s' % command

    # if command == '/door' and chat_id == -123571607:
    if command == '/door' and old_date != date and chat_id == -123571607:
        logger.debug("nuova richiesta! eseguo:")
        old_date = date
        # first = msg[len(msg)-1]['message']['chat']['first_name']
        # last = msg[len(msg)-1]['message']['chat']['last_name']

        logger.debug(chat_id)
        logger.debug("porta!")
        stringa = str(str(date) + ',' + str(command) + '\n')
        open('/home/pi/Documents/tagNFC_DB_server/theBrain/doorLog.txt','a+').write(stringa)
        open('/home/pi/Documents/tagNFC_DB_server/theBrain/bridge2brain.txt','w').write(stringa)
        bot.sendMessage(chat_id,"ok!")

    else:
        logger.debug("niente di nuovo")

a_bot = telepot.Bot('223540260:AAE5dNuHTt5F9m3gGHNxieghQgP58EzxilU')
