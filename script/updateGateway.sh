#!/bin/bash
PTH=`pwd`
echo "Sync git"
cd /home/pi/Documents/tagNFC_DB_server/
git pull

echo "upload it!"
cd /home/pi/Documents/tagNFC_DB_server/arduino/Gateway/
platformio run --upload-port /dev/ttyAMA0 -t upload

echo "come back"
cd $PTH
