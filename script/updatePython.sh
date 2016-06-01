#!/bin/bash
PTH=`pwd`
echo "Sync git"
cd /home/pi/Documents/tagNFC_DB_server/
git pull

echo "python as exe"
chmod 755 theBrain/theBrain.py
chmod 755 theBrain/goMonitor.sh
sudo cp theBrain/goMonitor.sh /etc/init.d
sudo update-rc.d goMonitor.sh defaults

echo "come back"
cd $PTH
