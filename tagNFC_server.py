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
            print "Tag received with ID:"

            linea = ser.readline()
            uid = linea.split(",")[4].split(" ")[0].split("x")[1] + linea.split(",")[4].split(" ")[1].split("x")[1] + linea.split(",")[4].split(" ")[2].split("x")[1] + linea.split(",")[4].split(" ")[3].split("x")[1]

            print uid

            try:
                print "Search for the person behind the tag..."
                cellTag = worksheet.find(uid)

            except:
                print "No one. So its a new fellow!"
                ser.write('n')
            else:
                print "Find one!"
                ser.write('o')
                print "Credits:"
                ser.write(worksheet.cell(cellTag.row, 3).value)
                print worksheet.cell(cellTag.row, 3).value
                print "Skills:"
                ser.write(worksheet.cell(cellTag.row, 4).value)
                print worksheet.cell(cellTag.row, 4).value
                ser.write('/n')

        elif (x != ''):
            linea = ser.readline()
            print linea


    except (KeyboardInterrupt, SystemExit):
        ser.close()
