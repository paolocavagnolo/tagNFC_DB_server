import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime

KEY_PATH = '/home/pi/Documents/techlab-tag-nfc-b3f2a2929d98.json'

class gDriveAPI(object):
    def __init__(self, worksheet_name, file_name):
        global ws_name = worksheet_name
        global fl_name = file_name
        self.scope = ['https://spreadsheets.google.com/feeds']
        self.credentials = ServiceAccountCredentials.from_json_keyfile_name(KEY_PATH, self.scope)
        self.file = gspread.authorize(self.credentials)
        self.sheet = self.file.open(fl_name)
        self.worksheet = self.sheet.worksheet(ws_name)

    def check(self):
        now = datetime.datetime.now()
        if self.file.auth.token_expiry < now:
            __init__(self, ws_name, fl_name)

    def find(self, stringa):
        check(self)
        return self.worksheet.find(stringa)

    def read_one(self, row, col):
        check(self)
        return self.worksheet.cell(row,col).value

    def read_row(self, row):
        check(self)
        return self.worksheet.row_values(row)

    def read_col(self, col):
        check(self)
        return self.worksheet.col_values(col)

    def write(self, row, col, value):
        check(self)
        return self.worksheet.update_cell(row,col,value)

    def write_line(row, linea, titoli):
        check(self)
        for item in linea:
            j = 0
            for titolo in titoli:
                j = j + 1
                if item == titolo:
                    self.worksheet.update_cell(row,j,linea[item])
