# -*- coding: utf-8 -*-
import serial
import json
import datetime
import struct
import pymongo
import telepot
from pymongo import MongoClient
import gspread
from oauth2client.service_account import ServiceAccountCredentials


SYSTEM_PATH = '/home/pi/Documents/'
PATH_KEYS = SYSTEM_PATH + 'keys.txt'
fkey=open(PATH_KEYS,'r')
fkeylines=fkey.readlines()
GDRIVE_API_KEY = SYSTEM_PATH + fkeylines[1].split('\n')[0]
MONGODB_CLIENT_MLAB = fkeylines[3].split('\n')[0]
TELEGRAM_BRIDGE = SYSTEM_PATH + fkeylines[5].split('\n')[0]
ENERGYLOG = SYSTEM_PATH + fkeylines[7].split('\n')[0]
fkey.close()


# readFromSerial(RFmsg):

ser = serial.Serial('/dev/ttysAMA0', 115200, timeout=.5)

def readFromSerial(RFmsg):
    if ser.is_open:
        pl = ser.readline().rstrip()
        if len(pl) > 2 and pl[0] == '<' and pl[1] == ',':
                RFmsg = pl
                return True, RFmsg
        else:
            return False
    else:
        ser.open()
        readFromSerial(RFmsg)


# readFromTelegram():
def readFromTelegram():
    if os.path.isfile(TELEGRAM_BRIDGE):
        return True
    else:
        return False


# msgIn = radioPkt(RFmsg)

class radioPkt(object):
    def __init__(self, payload):
        self.payload_in = payload
        self.abs = payload.split(',')[1]
        self.ids = payload.split(',')[2]
        self.idr = payload.split(',')[3]
        self.RSSI = payload.split(',')[4]
        if self.ids == '3':
            self.idm = 'd'
        else:
            self.idm = payload.split(',')[5].decode("HEX")
        self.date = datetime.datetime.now()

        if self.idm == 'n':
            self.tag = ''.join(payload.split(',')[6:12])

        elif self.idm == 'e':
            self.idphase = payload.split(',')[6].decode("HEX")
            self.count = bytes2float(payload.split(',')[7:11])


# msgIn = telegramPkt()
# [{u'message': {u'chat': {u'first_name': u'Nick',
#                          u'id': 999999999,
#                          u'last_name': u'Lee',
#                          u'type': u'private'},
#                u'date': 1444723969,
#                u'from': {u'first_name': u'Nick',
#                          u'id': 999999999,
#                          u'last_name': u'Lee'},
#                u'message_id': 4015,
#                u'text': u'Hello'},
#   u'update_id': 100000000}]

class telegramPkt(object):
    def __init__():
        with open(TELEGRAM_BRIDGE) as data_file:
            data = json.load(data_file)

        self.cmd = data[:-1]['message']['text'].split('\\')[1]
        self.chatId = data[:-1]['message']['chat']['id']
        self.chatFirst = data[:-1]['message']['chat']['first_name']
        self.fromFirst = data[:-1]['message']['from']['first_name']
        self.fromLast = data[:-1]['message']['from']['last_name']
        self.idm = 'b'
        self.date = datetime.datetime.now()

class answerTelegram(object):
    def __init__():
        self.idr = self.ids
        self.ids = 1
        self.date = datetime.datetime.now()
        self.idr = 4
        self.payload_out = 'd'

# msgOut = telegramPrs(msgIn)

bot = telepot.Bot('223540260:AAE5dNuHTt5F9m3gGHNxieghQgP58EzxilU')

def telegramPrs(msgIn):
    msgOut = answerTelegram()



# dbLog.write(msg.__dict__)

class mongoDB(object):

    def __init__(self, collection, database):
        self.client = MongoClient(MONGODB_CLIENT_MLAB)
        self.db = self.client[database]
        self.collection = self.db[collection]

    def close(self):
        self.client.close()

    def read(self, document):
        c = self.collection.find(document).count()
        f = self.collection.find(document)
        return c, f

    def write(self, document):
        return self.collection.insert(document)

    def read_last_N(self, N):
        alls = self.collection.find().skip(self.collection.count() - N)
        malloppo = []
        for item in alls:
            malloppo.append(item)
        return malloppo



# msgOut = checkMember(msgIn)

class gDriveAPI(object):

    def __init__(self, worksheet_name, file_name):
        self.ws_name = worksheet_name
        self.fl_name = file_name
        self.scope = ['https://spreadsheets.google.com/feeds']
        self.credentials = ServiceAccountCredentials.from_json_keyfile_name(GDRIVE_API_KEY, self.scope)
        self.file = gspread.authorize(self.credentials)
        self.sheet = self.file.open(self.fl_name)
        self.worksheet = self.sheet.worksheet(self.ws_name)

    def check(self):
        now = datetime.datetime.now()
        now = now.replace(hour = now.hour - 2)
        if self.file.auth.token_expiry < now:
            print "il token e' minore di adesso"
            print self.file.auth.token_expiry
            print now
            self.__init__(self.ws_name, self.fl_name)

    def find(self, stringa):
        self.check()
        try:
            return self.worksheet.find(stringa)
        except:
            return self.worksheet.find('00000000')

    def read_one(self, row, col):
        self.check()
        return self.worksheet.cell(row,col).value

    def read_row(self, row):
        self.check()
        return self.worksheet.row_values(row)

    def read_col(self, col):
        self.check()
        return self.worksheet.col_values(col)

    def write(self, row, col, value):
        self.check()
        return self.worksheet.update_cell(row,col,value)

    def write_line(self, row, linea, titoli):
        self.check()
        for item in linea:
            j = 0
            for titolo in titoli:
                j = j + 1
                if item == titolo:
                    self.worksheet.update_cell(row,j,linea[item])

class answer(radioPkt):
    def __init__(self, payload, cr=0, sk=0):
        super(answer, self).__init__(payload)
        self.idr = self.ids
        self.ids = 1
        self.date = datetime.datetime.now()
        if self.idm == 'n' or self.idm == 't':
            self.cr = cr
            self.cr_b = float2bytes(float(cr))
            self.sk = sk
            self.payload_out = str(self.cr_b) + str(self.sk)
        if self.idm == 'b':
            self.idr = 4
            self.payload_out = 'd'


def checkMember(msgIn, gUser):
    cellTag = gUser.find(msgIn.tag[0:8])
    msgOut = answer(msgIn.payload_in,gUser.read_one(cellTag.row, 3),gUser.read_one(cellTag.row, 4))
    return msgOut


# openSession(msgIn)

def openSession(msgIn, id_session, gSes, gUser):
    cellTag = gUser.find(msgIn.tag[0:8])
    gSes.write(id_session+1,1,id_session) #id
    gSes.write(id_session+1,2,msgIn.date) #data
    gSes.write(id_session+1,3,gUser.read_one(cellTag.row, 8)) #mail
    gSes.write(id_session+1,4,0) #cr


# msgOut = updateMember(msgIn)

def updateMember(msgIn, gUser, gSes, id_session):
    cellTag = gUser.find(msgIn.tag[0:8])

    cr = float(gUser.read_one(cellTag.row, 3))
    sk = gUser.read_one(cellTag.row, 4)
    cr_new = cr - (0.2-(0.1*int(sk)))

    msgOut = answer(msgIn.payload_in,cr_new,sk)
    gUser.write(cellTag.row, 3, cr_new)

    gSes.write(id_session+1,4,float(gSes.read_one(id_session+1,4))+(0.2-(0.1*int(sk))))

    return msgOut

# updateEnergy(msgIn)

def updateEnergy(msgIn):
    open(ENERGYLOG,'a+',0).write(str(msgIn.date) + ',' + str(msgIn.idphase) + ',' + str(msgIn.count) + '\n')
    #os.system("plotData.sh")


# goReal(msgOut)

def goReal(msgOut):

    ser.write('i'+msgOut.idr+'\0')
    ser.flush()
    time.sleep(1)

    ser.write('j'+msgOut.payload_out+'\0')
    ser.flush()
