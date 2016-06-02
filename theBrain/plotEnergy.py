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
  buffer_file = "/home/pi/Documents/tagNFC_DB_server/theBrain/energyBuffer.log"
  lines = []
  with open(buffer_file, "r") as f:
      lines = f.readlines()
  # with open(buffer_file, "w") as f:
  #     f.truncate()
  f.close()
  lines = map(lambda x: x.rstrip(), lines)
  return lines


lines = readFromFile()

i=0
for line in lines:
    data = lines[i].split(',')[0]
    idphase = lines[i].split(',')[1]
    count = lines[i].split(',')[2]
    if idphase == 'a':
        data2web(data,count,' ',' ')
    elif idphase == 'b':
        data2web(data,' ',count,' ')
    elif idphase == 'c':
        data2web(data,' ',' ',count)
    i=i+1
