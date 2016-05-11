import plotly
print plotly.__version__  # version >1.9.4 required

from plotly.graph_objs import Scatter, Layout
import struct

def byte2float( bytess ):

    data = bytess
    if (len(data[0])<2):
        data[0] = '0'+data[0]
    if (len(data[1])<2):
        data[1] = '0'+data[1]
    if (len(data[2])<2):
        data[2] = '0'+data[2]
    if (len(data[3])<2):
        data[3] = '0'+data[3]
    byte1 = ord(data[0].decode("HEX"))
    byte2 = ord(data[1].decode("HEX"))
    byte3 = ord(data[2].decode("HEX"))
    byte4 = ord(data[3].decode("HEX"))

    bytecc = [byte4, byte3, byte2, byte1]
    b = ''.join(chr(i) for i in bytecc)

    return float("{0:.2f}".format(struct.unpack('>f', b)[0]))

#collect point
yA = []
xA = []
yB = []
xB = []
yC = []
xC = []

with open('log.txt','r') as f:
    for line in f:
        if line.split(',')[5].decode("HEX") == 'a':
            aa = (byte2float(line.split(',')[6:10]))
            yA.append(aa)
            xA.append(line.split(',')[1])
        elif line.split(',')[5].decode("HEX") == 'b':
            bb = (byte2float(line.split(',')[6:10]))
            yB.append(bb)
            xB.append(line.split(',')[1])
        elif line.split(',')[5].decode("HEX") == 'c':
            cc = (byte2float(line.split(',')[6:10]))
            yC.append(cc)
            xC.append(line.split(',')[1])
        else:
            print "error"

yA = [e / max(yA) for e in yA]
yB = [e / max(yB) for e in yB]
yC = [e / max(yC) for e in yC]


#divide point in trace
traceA = Scatter(
    x = xA,
    y = yA
)
traceB = Scatter(
    x = xB,
    y = yB
)
traceC = Scatter(
    x = xC,
    y = yC
)

data = [traceA,traceB,traceC]

#plotit
plotly.offline.plot(data,filename='basic')
