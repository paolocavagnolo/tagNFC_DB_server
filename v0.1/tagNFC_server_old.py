#!/usr/bin/python

import serial
import gspread
import struct
import logging
import sys
import time

from oauth2client.service_account import ServiceAccountCredentials


#log part
try:
    logging.basicConfig(filename='/home/pi/Documents/logs/'+sys.argv[1]+'.log',format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p', level=logging.INFO)
except:
    print "The name of the log file! pass it as an argument"
#debug / info / warning
logging.info('New beginning')


#gspread part
scope = ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_name('/home/pi/techlab-tag-nfc-b3f2a2929d98.json', scope)
gc = gspread.authorize(credentials)
logging.info(gc)
sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1KWxCi7tny8uxo4TmzjNnVuNj5eGRVngwFD2gxIX5qfw/edit?usp=sharing')
worksheet = sh.worksheet("soci")
worksheet_log = sh.worksheet("log_laser")
cellTag = ""
Cr = 0
Sk = 0

#serial part
ser = serial.Serial('/dev/ttyAMA0',115200,timeout=1)
logging.info(ser)

#time part
t0 = time.time()


logging.info("Ready!")
while True:
    try:
        #read from serial
        x = ser.read()

        #select lines
        # from Gateway a tagID
        if (x == '#'):
            t0 = time.time()
            logging.info("PY: Tag received with ID:")

            linea = ser.readline()
            uid = linea.split(",")[4].split(" ")[0].split("x")[1] + linea.split(",")[4].split(" ")[1].split("x")[1] + linea.split(",")[4].split(" ")[2].split("x")[1] + linea.split(",")[4].split(" ")[3].split("x")[1]

            logging.info(uid)

            try:
                logging.info("PY: Search for the person behind the tag...")
                cellTag = worksheet.find(uid)

            except:
                logging.info("PY: No one. So its a new fellow!")
                ser.write('n')
                ser.flush()
            else:
                logging.info("PY: Find one!")
                ser.write('c' + struct.pack('>B', float(worksheet.cell(cellTag.row, 3).value)))
                ser.flush()
                logging.info("PY: Credits:")
                logging.info(worksheet.cell(cellTag.row, 3).value)
                ser.write('s' + struct.pack('>B', int(worksheet.cell(cellTag.row, 4).value)))
                ser.flush()
                logging.info("PY: Skills:")
                logging.info(worksheet.cell(cellTag.row, 4).value)

        elif (x == '-'):
            t0 = time.time()
            Cr = float(worksheet.cell(cellTag.row, 3).value)
            Sk = int(worksheet.cell(cellTag.row, 4).value)
            worksheet.update_cell(cellTag.row, 3, Cr-(0.2-(0.1*Sk)))
            #print str(Cr) + " - " + str(Sk) + str(Cr-(0.2-(0.1*Sk)))
            ser.write('c' + struct.pack('>B', float(worksheet.cell(cellTag.row, 3).value)))
            logging.info("PY: Credits:")
            logging.info(worksheet.cell(cellTag.row, 3).value)
            ser.write('s' + struct.pack('>B', float(worksheet.cell(cellTag.row, 4).value)))
            ser.flush()
            logging.info("PY: Skills:")
            logging.info(worksheet.cell(cellTag.row, 4).value)

        elif (x != ''):
            linea = ser.readline()
            logging.info(linea)

        else:
            time.sleep(2)


    except (KeyboardInterrupt, SystemExit):
        ser.close()

    if ((time.time() - t0) > 600):
        logging.info("Reset connections GDrive / Serial")
        ser.close()
        scope = ['https://spreadsheets.google.com/feeds']
        credentials = ServiceAccountCredentials.from_json_keyfile_name('/home/pi/techlab-tag-nfc-b3f2a2929d98.json', scope)
        gc = gspread.authorize(credentials)
        sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1KWxCi7tny8uxo4TmzjNnVuNj5eGRVngwFD2gxIX5qfw/edit?usp=sharing')
        worksheet = sh.worksheet("soci")
        worksheet_log = sh.worksheet("log_laser")
        ser = serial.Serial('/dev/ttyAMA0',115200,timeout=1)
        t0 = time.time()
