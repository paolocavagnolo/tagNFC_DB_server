import serial
import time
import struct

prompt = '> '

ser = serial.Serial('/dev/ttyAMA0',115200) #open a serial connection to talk with the gateway

def float2bytes( data ):
    vals = list(struct.pack('<f', data))
    c_vals = []
    for num in vals:
        if num == '\x00':
            c_vals.append('0')
        else:
            c_vals.append(num)

    return ''.join(c_vals)

print "Count for A?"
a_count = raw_input(prompt)

ser.write('i'+'4'+'\0')
time.sleep(1)
ser.write('j'+float2bytes(float(a_count))+'\0')

print "Count for B?"
b_count = raw_input(prompt)

ser.write('i'+'4'+'\0')
time.sleep(1)
ser.write('j'+float2bytes(float(b_count))+'\0')

print "Count for C?"
c_count = raw_input(prompt)

ser.write('i'+'4'+'\0')
time.sleep(1)
ser.write('j'+float2bytes(float(c_count))+'\0')
