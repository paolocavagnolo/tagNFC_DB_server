import serial
import gspread
from oauth2client.service_account import ServiceAccountCredentials

#gspread part
scope = ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_name('/home/pi/techlab-tag-nfc-b3f2a2929d98.json', scope)
gc = gspread.authorize(credentials)
sht1 = gc.open_by_url('https://docs.google.com/spreadsheets/d/1KWxCi7tny8uxo4TmzjNnVuNj5eGRVngwFD2gxIX5qfw/edit?usp=sharing')

#serial part
ser = serial.Serial('/dev/ttyAMA0',115200,timeout=1)
cc = 0;

while True:
    try:
        #read from serial
        x = ser.read()

        #select lines
        if (x == '#'):
            linea = ser.readline()
            uid = linea.split(",")[4].split(" ")[0].split("x")[1] + linea.split(",")[4].split(" ")[1].split("x")[1] + linea.split(",")[4].split(" ")[2].split("x")[1] + linea.split(",")[4].split(" ")[3].split("x")[1]
            cc = 1
            print uid

        if (cc == 1):
            print muterun_js('/home/pi/Database/read_gsheet.js 2 3')
            cc = 0;

    except (KeyboardInterrupt, SystemExit):
        ser.close()
