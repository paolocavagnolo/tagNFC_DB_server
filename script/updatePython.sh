#!/bin/bash
PTH=`pwd`
echo "Sync git"
cd /home/pi/Documents/tagNFC_DB_server/
git pull

echo "python as exe"

sudo cp theBrain/goMonitor.sh /etc/init.d/
sudo cp theBrain/theBrain.py /usr/local/bin/theBrain/

sudo chmod 755 /usr/local/bin/theBrain/theBrain.py
sudo chmod 755 /etc/init.d/goMonitor.sh

cd /etc/init.d/
sudo update-rc.d goMonitor.sh defaults

echo "come back"
cd $PTH
