#!/bin/bash
clear
echo "Take the hex file"
svn export https://github.com/paolocavagnolo/tagNFC_DB_server/trunk/gateway.hex --force /home/pi/Documents/beep/.build/uno/
rm /home/pi/Documents/beep/.build/uno/firmware.hex
mv /home/pi/Documents/beep/.build/uno/gateway.hex /home/pi/Documents/beep/.build/uno/firmware.hex
echo "upload it!"
cd /home/pi/Documents/beep/
ino upload -p /dev/ttyAMA0
