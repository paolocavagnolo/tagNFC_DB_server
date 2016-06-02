import fileinput

def data2web( data, a, b, c ):

    processing_foo1s = False
    last_row = "<tr><td>Data</td><td>A</td><td>B</td><td>C</td></tr>"
    full = "<tr><td>" + data + "</td><td>" + str(a) + "</td><td>" + str(b) + "</td><td>" + str(c) + "</td></tr>"

    for line in fileinput.input('panel.html', inplace=1):
      if line.startswith(last_row):
        processing_foo1s = True
      else:
        if processing_foo1s:
          print full
        processing_foo1s = False
      print line,

def readFromFile():
  arduFile = "/home/pi/Documents/tagNFC_DB_server/theBrain/energyBuffer.log"
  lines = []
  with open(arduFile, "r") as f:
      lines = f.readlines()
  # with open(arduFile, "w") as f:
  #     f.truncate()
  f.close()
  lines = map(lambda x: x.rstrip(), lines)
  return lines

lines = readFromFile()



# if a_msg.idphase == 'a':
#     data2web(a_msg.date.strftime('%d/%m/%y %H:%M:%S'),a_msg.count,' ',' ')
# elif a_msg.idphase == 'b':
#     data2web(a_msg.date.strftime('%d/%m/%y %H:%M:%S'),' ',a_msg.count,' ')
# elif a_msg.idphase == 'c':
#     data2web(a_msg.date.strftime('%d/%m/%y %H:%M:%S'),' ',' ',a_msg.count)
