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
