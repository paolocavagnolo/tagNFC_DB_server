import serial
import gspread
from oauth2client.service_account import ServiceAccountCredentials

#gspread part
scope = ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_name('/home/pi/techlab-tag-nfc-b3f2a2929d98.json', scope)
gc = gspread.authorize(credentials)
sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1KWxCi7tny8uxo4TmzjNnVuNj5eGRVngwFD2gxIX5qfw/edit?usp=sharing')
worksheet = sh.get_worksheet(0)

#serial part
ser = serial.Serial('/dev/ttyAMA0',115200,timeout=1)

print "Ready!"
while True:
    try:
        #read from serial
        x = ser.read()

        #select lines
        # from Gateway a tagID
        if (x == '#'):
            print "PY: Tag received with ID:"

            linea = ser.readline()
            uid = linea.split(",")[4].split(" ")[0].split("x")[1] + linea.split(",")[4].split(" ")[1].split("x")[1] + linea.split(",")[4].split(" ")[2].split("x")[1] + linea.split(",")[4].split(" ")[3].split("x")[1]

            print uid

            try:
                print "PY: Search for the person behind the tag..."
                cellTag = worksheet.find(uid)

            except:
                print "PY: No one. So its a new fellow!"
                ser.write('n')
            else:
                print "PY: Find one!"
                ser.write('o' + 'a' + 'b')
                print "PY: Credits:"
                print worksheet.cell(cellTag.row, 3).value
                print "PY: Skills:"
                print worksheet.cell(cellTag.row, 4).value

        elif (x != ''):
            linea = ser.readline()
            print linea


    except (KeyboardInterrupt, SystemExit):
        ser.close()
