#!/bin/bash
PTH=`pwd`
echo "Sync git"
cd /home/pi/Documents/tagNFC_DB_server/
git pull

echo "python!"
python /home/pi/Documents/tagNFC_DB_server/tagNFC_server.py

echo "come back"
cd $PTH
