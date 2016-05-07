import struct

def byte2float( bytess ):

    data = bytess
    byte1 = ord(data[2].decode("HEX"))
    byte2 = ord(data[3].decode("HEX"))
    byte3 = ord(data[4].decode("HEX"))
    byte4 = ord(data[5].decode("HEX"))

    bytecc = [byte4, byte3, byte2, byte1]
    b = ''.join(chr(i) for i in bytecc)

    return struct.unpack('>f', b)[0]



linea = "<,1553,4,1,65,63,4,7,4F,42,-39,>"
message = [0,0,0,0,0,0]


abss = int(linea.split(",")[1])
ids = int(linea.split(",")[2])
idr = int(linea.split(",")[3])
message[0] = linea.split(",")[4]
message[1] = linea.split(",")[5]
message[2] = linea.split(",")[6]
if (len(message[2])<2):
    message[2] = '0'+message[2]
message[3] = linea.split(",")[7]
if (len(message[3])<2):
    message[3] = '0'+message[3]
message[4] = linea.split(",")[8]
if (len(message[4])<2):
    message[4] = '0'+message[4]
message[5] = linea.split(",")[9]
if (len(message[5])<2):
    message[5] = '0'+message[5]
RSSI = int(linea.split(",")[10])

print byte2float( message )
