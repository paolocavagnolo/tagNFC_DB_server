import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime

KEY_PATH = '/home/pi/Documents/techlab-tag-nfc-b3f2a2929d98.json'


class gDriveAPI(object):

    def __init__(self, worksheet_name, file_name):
        self.ws_name = worksheet_name
        self.fl_name = file_name
        self.scope = ['https://spreadsheets.google.com/feeds']
        self.credentials = ServiceAccountCredentials.from_json_keyfile_name(KEY_PATH, self.scope)
        self.file = gspread.authorize(self.credentials)
        self.sheet = self.file.open(fl_name)
        self.worksheet = self.sheet.worksheet(ws_name)

    def check(self):
        now = datetime.datetime.now()
        if self.file.auth.token_expiry < now:
            print "il token è minore di adesso"
            print self.file.auth.token_expiry
            print now
            self.__init__(self.ws_name, self.fl_name)

    def find(self, stringa):
        self.check()
        return self.worksheet.find(stringa)

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

    def write_line(row, linea, titoli):
        self.check()
        for item in linea:
            j = 0
            for titolo in titoli:
                j = j + 1
                if item == titolo:
                    self.worksheet.update_cell(row,j,linea[item])
