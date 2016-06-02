#!/bin/bash
PTH=`pwd`
echo "Take data from buffer file and manage it, then truncate the file"
cd /home/pi/Documents/tagNFC_DB_server/theBrain
python plotEnergy.py

echo "Copy file to the apache serve index.html"
sudo cp panel.html /var/www/html/
cd /var/www/html/
sudo rm index.html
sudo mv panel.html index.html

echo "come back"
cd $PTH
