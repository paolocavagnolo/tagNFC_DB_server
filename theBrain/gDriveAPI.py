import gspread
from oauth2client.service_account import ServiceAccountCredentials

KEY_PATH = '/home/pi/Documents/techlab-tag-nfc-b3f2a2929d98.json'

class gDriveAPI(object):
    def __init__(self, worksheet_name, file_name):
        self.scope = ['https://spreadsheets.google.com/feeds']
        self.credentials = ServiceAccountCredentials.from_json_keyfile_name(KEY_PATH, self.scope)
        self.file = gspread.authorize(self.credentials)
        self.sheet = self.file.open(file_name)
        self.worksheet = self.sheet.worksheet(worksheet_name)

    def find(self, stringa):
        return self.worksheet.find(stringa)

    def read_one(self, row, col):
        return self.worksheet.cell(row,col).value

    def read_row(self, row):
        return self.worksheet.row_values(row)

    def read_col(self, col):
        return self.worksheet.col_values(col)

    def write(self, row, col, value):
        return self.worksheet.update_cell(row,col,value)

    def write_line(row, linea, titoli):
        for item in linea:
            j = 0
            for titolo in titoli:
                j = j + 1
                if item == titolo:
                    self.worksheet.update_cell(row,j,linea[item])
