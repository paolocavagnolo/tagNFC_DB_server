import serial
import gspread
import struct
from oauth2client.service_account import ServiceAccountCredentials
log_file = open("/home/pi/Documents/log_tag.log","a")

#gspread part
scope = ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_name('/home/pi/techlab-tag-nfc-b3f2a2929d98.json', scope)
gc = gspread.authorize(credentials)
sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1KWxCi7tny8uxo4TmzjNnVuNj5eGRVngwFD2gxIX5qfw/edit?usp=sharing')
worksheet = sh.worksheet("soci")
worksheet_log = sh.worksheet("log_laser")
cellTag = ""
Cr = 0
Sk = 0

#serial part
ser = serial.Serial('/dev/ttyAMA0',115200,timeout=1)


log_file.write("Ready!")
while True:
    try:
        #read from serial
        x = ser.read()

        #select lines
        # from Gateway a tagID
        if (x == '#'):
            log_file.write("PY: Tag received with ID:")

            linea = ser.readline()
            uid = linea.split(",")[4].split(" ")[0].split("x")[1] + linea.split(",")[4].split(" ")[1].split("x")[1] + linea.split(",")[4].split(" ")[2].split("x")[1] + linea.split(",")[4].split(" ")[3].split("x")[1]

            log_file.write(uid)

            try:
                log_file.write("PY: Search for the person behind the tag...")
                cellTag = worksheet.find(uid)

            except:
                log_file.write("PY: No one. So its a new fellow!")
                ser.write('n')
                ser.flush()
            else:
                log_file.write("PY: Find one!")
                ser.write('c' + struct.pack('>B', float(worksheet.cell(cellTag.row, 3).value)))
                ser.flush()
                log_file.write("PY: Credits:")
                log_file.write(worksheet.cell(cellTag.row, 3).value)
                ser.write('s' + struct.pack('>B', int(worksheet.cell(cellTag.row, 4).value)))
                ser.flush()
                log_file.write("PY: Skills:")
                log_file.write(worksheet.cell(cellTag.row, 4).value)

        elif (x == '-'):
            Cr = float(worksheet.cell(cellTag.row, 3).value)
            Sk = int(worksheet.cell(cellTag.row, 4).value)
            worksheet.update_cell(cellTag.row, 3, Cr-(0.2-(0.1*Sk)))
            #print str(Cr) + " - " + str(Sk) + str(Cr-(0.2-(0.1*Sk)))
            ser.write('c' + struct.pack('>B', float(worksheet.cell(cellTag.row, 3).value)))
            log_file.write("PY: Credits:")
            log_file.write(worksheet.cell(cellTag.row, 3).value)
            ser.write('s' + struct.pack('>B', float(worksheet.cell(cellTag.row, 4).value)))
            ser.flush()
            log_file.write("PY: Skills:")
            log_file.write(worksheet.cell(cellTag.row, 4).value)

        elif (x != ''):
            linea = ser.readline()
            log_file.write(linea)


    except (KeyboardInterrupt, SystemExit):
        ser.close()
