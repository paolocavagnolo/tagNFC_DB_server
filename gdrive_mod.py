#   Module for interact with Google Drive API   #
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_name('/home/pi/Documents/techlab-tag-nfc-b3f2a2929d98.json', scope)


def find( string ):
    try:
        gc = gspread.authorize(credentials)
        sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1KWxCi7tny8uxo4TmzjNnVuNj5eGRVngwFD2gxIX5qfw/edit?usp=sharing')
        if credentials.access_token_expired:
            gc.login()

        ###function
        worksheet = sh.worksheet("soci")
        return worksheet.find(string)

    except Exception, e:
        traceback.print_exc()


def read_one( row, col ):
    try:
        gc = gspread.authorize(credentials)
        sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1KWxCi7tny8uxo4TmzjNnVuNj5eGRVngwFD2gxIX5qfw/edit?usp=sharing')
        if credentials.access_token_expired:
            gc.login()

        ###function
        worksheet = sh.worksheet("soci")
        return worksheet.cell(row, col).value

    except Exception, e:
        traceback.print_exc()


def read_row( row ):
    try:
        gc = gspread.authorize(credentials)
        sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1KWxCi7tny8uxo4TmzjNnVuNj5eGRVngwFD2gxIX5qfw/edit?usp=sharing')
        if credentials.access_token_expired:
            gc.login()

        ###function
        worksheet = sh.worksheet("soci")
        return worksheet.row_values(row)

    except Exception, e:
        traceback.print_exc()


def read_col_log( col ):
    try:
        gc = gspread.authorize(credentials)
        sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1KWxCi7tny8uxo4TmzjNnVuNj5eGRVngwFD2gxIX5qfw/edit?usp=sharing')
        if credentials.access_token_expired:
            gc.login()

        ###function
        worksheet = sh.worksheet("log")
        return worksheet.col_values(col)

    except Exception, e:
        traceback.print_exc()


def read_row_log( row ):
    try:
        gc = gspread.authorize(credentials)
        sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1KWxCi7tny8uxo4TmzjNnVuNj5eGRVngwFD2gxIX5qfw/edit?usp=sharing')
        if credentials.access_token_expired:
            gc.login()

        ###function
        worksheet = sh.worksheet("log")
        return worksheet.row_values(row)

    except Exception, e:
        traceback.print_exc()


def write( row, col, value):
    try:
        gc = gspread.authorize(credentials)
        sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1KWxCi7tny8uxo4TmzjNnVuNj5eGRVngwFD2gxIX5qfw/edit?usp=sharing')
        if credentials.access_token_expired:
            gc.login()

        ###function
        worksheet = sh.worksheet("soci")
        return worksheet.update_cell(row, col, value)

    except Exception, e:
        traceback.print_exc()


def write_log( row, col, value):
    try:
        gc = gspread.authorize(credentials)
        sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1KWxCi7tny8uxo4TmzjNnVuNj5eGRVngwFD2gxIX5qfw/edit?usp=sharing')
        if credentials.access_token_expired:
            gc.login()

        ###function
        worksheet = sh.worksheet("log")
        return worksheet.update_cell(row, col, value)

    except Exception, e:
        traceback.print_exc()


def update_linea( row , linea, titoli):

    for item in linea:
        print "guardo %r" % item,
        j = 0
        for titolo in titoli:
            print "e lo confronto con %r" % titolo
            j = j + 1
            if item == titolo:
                try:
                    gc = gspread.authorize(credentials)
                    sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1KWxCi7tny8uxo4TmzjNnVuNj5eGRVngwFD2gxIX5qfw/edit?usp=sharing')
                    if credentials.access_token_expired:
                        gc.login()

                    ###function
                    write_log(row,j,linea[item])

                except Exception, e:
                    traceback.print_exc()


def read_session( row, col):
    try:
        gc = gspread.authorize(credentials)
        sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1KWxCi7tny8uxo4TmzjNnVuNj5eGRVngwFD2gxIX5qfw/edit?usp=sharing')
        if credentials.access_token_expired:
            gc.login()

        ###function
        worksheet = sh.worksheet("open_session")
        return worksheet.cell(row, col).value

    except Exception, e:
        traceback.print_exc()


def write_session( row, col, value):
    try:
        gc = gspread.authorize(credentials)
        sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1KWxCi7tny8uxo4TmzjNnVuNj5eGRVngwFD2gxIX5qfw/edit?usp=sharing')
        if credentials.access_token_expired:
            gc.login()

        ###function
        worksheet = sh.worksheet("open_session")
        return worksheet.update_cell(row, col, value)

    except Exception, e:
        traceback.print_exc()
