#   Module for interact with Google Drive API   #
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_name('/home/pi/Documents/techlab-tag-nfc-b3f2a2929d98.json', scope)
gc = gspread.authorize(credentials)
sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1KWxCi7tny8uxo4TmzjNnVuNj5eGRVngwFD2gxIX5qfw/edit?usp=sharing')

def open():
    scope = ['https://spreadsheets.google.com/feeds']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('/home/pi/Documents/techlab-tag-nfc-b3f2a2929d98.json', scope)
    gc = gspread.authorize(credentials)
    sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1KWxCi7tny8uxo4TmzjNnVuNj5eGRVngwFD2gxIX5qfw/edit?usp=sharing')

def find( string ):

    worksheet = sh.worksheet("soci")
    return worksheet.find(string)

def read_one( row, col ):

    worksheet = sh.worksheet("soci")
    return worksheet.cell(row, col).value

def read_row( row ):

    worksheet = sh.worksheet("soci")
    return worksheet.row_values(row)

def write( row, col, value):

    worksheet = sh.worksheet("soci")
    return worksheet.update_cell(row, col, value)
