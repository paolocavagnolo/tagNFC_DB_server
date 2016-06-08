s = ['\x00', '\x00', '\xc7', 'B']
a = '\x00'

print s

for n,i in enumerate(s):
    if i==a:
        s[n]='0x00'

print s
