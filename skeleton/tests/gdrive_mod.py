#   Module for interact with Google Drive API   #

import gspread

from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_name('/home/pi/Documents/techlab-tag-nfc-b3f2a2929d98.json', scope)

gc = gspread.authorize(credentials)
sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1KWxCi7tny8uxo4TmzjNnVuNj5eGRVngwFD2gxIX5qfw/edit?usp=sharing')
worksheet = sh.worksheet("soci")

def find( string ):
    return worksheet.find(string)

def read( row, col ):
    return worksheet.cell(row, col).value

def write( row, col, value):
    return worksheet.update_cell(row, col, value)
