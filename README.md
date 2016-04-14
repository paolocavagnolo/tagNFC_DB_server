# tagNFC_DB_server

An open source system to manage machines in a cool makerspace!

The system is composed by nodes and 1 gateway. The gateway is a arduino YUN with an RFM69 moteino board.
Each node has at least 1 moteino board and a NFC tag shield.

## Gateway

https://mongopi.wordpress.com/2012/11/25/installation/

I'm using Raspberry PI 3.
Download raspbian from [here] (https://www.raspberrypi.org/downloads/raspbian/)

Follow all the instructions [here](https://www.raspberrypi.org/documentation/installation/installing-images/)

Resize to the max size
      sudo raspi-config
      --resize

update

      sudo apt-get update
      sudo apt-get upgrade
      sudo apt-get dist-upgrade
      sudo rpi-update
      sudo dpkg-reconfigure tzdata

from https://openenergymonitor.org/emon/node/12311

      sudo nano /boot/config.txt
      add core_freq=250

test UART

      sudo apt-get install minicom
      sudo minicom -D /dev/ttyAMA0 -b115200

prevent rpi3 to use UART

      sudo nano /boot/cmdline.txt
      dwc_otg.lpm_enable=0 console=serial1,115200  console=tty1 root=/dev/mmcblk0p2  kgdboc=serial1,115200 rootfstype=ext4 elevator=deadline fsck.repair=yes  rootwait

install subversion

      sudo apt-get install subversion

download the last python code

      svn export https://github.com/paolocavagnolo/tagNFC_DB_server/trunk/Gateway --force

## MongoDB on pi
http://andyfelong.com/2016/01/mongodb-3-0-9-binaries-for-raspberry-pi-2-jessie/

## Arduino on pi
https://github.com/amperka/ino

## Upload sketch from rpi3

      copy the hex file to .build/uno/firmware.hex (changing the name with firmware!)
      move to the project folder
      ino upload -p /dev/ttyAMA0



## Google sheet

https://www.nczonline.net/blog/2014/03/04/accessing-google-spreadsheets-from-node-js/

install nodejs

      sudo apt-get install nodejs npm

and

      wget https://nodejs.org/dist/v4.2.4/node-v4.2.4-linux-armv6l.tar.gz
      sudo mv node-v4.2.4-linux-armv6l.tar.gz /opt
      cd /opt
      sudo tar -xzf node-v4.2.4-linux-armv6l.tar.gz
      sudo mv node-v4.2.4-linux-armv6l nodejs
      sudo rm node-v4.2.4-linux-armv6l.tar.gz
      sudo ln -s /opt/nodejs/bin/node /usr/bin/node
      sudo ln -s /opt/nodejs/bin/npm /usr/bin/npm


https://github.com/codeforamerica/ohana-api/wiki/Automatically-generate-CSV-files-from-a-HSDS-Google-spreadsheet

      rake ohana:csv[https://docs.google.com/spreadsheets/d/1gBOByKgaDgbneWOBalxZ5jihJVV1iUFKuytqGVUG380/edit?usp=sharing]


## The script!

http://sweetme.at/2014/02/17/a-simple-approach-to-execute-a-node.js-script-from-python/


## Autoupdating

1) take info from gsheet to csv
2) csv to json
3) json to MongoDB
4) fine!

      rake ohana:csv[https://docs.google.com/spreadsheets/d/1gBOByKgaDgbneWOBalxZ5jihJVV1iUFKuytqGVUG380/edit?usp=sharing]

      python import_csv.py

      mongoimport --db techlab --collection soci --drop --file out.json





## Laser node
###Hacking the Laser
![Alt text](https://lh3.googleusercontent.com/XCoaaOT6O4BzO5U8wtSX5OgKLz_5uHQfqf0ip7A4G7SFzWbD5I9IVt8VVpTohM7vxBachwNntntgR7AXrMmXbZT2xcmWbJHFiKCxw51UEXsCrnUGEzItq08hpOqjPtaAMyVmiOfyLbpttHSsaZAfdHApaE0IhWU2CuKlxmATBdZQVPPnSq5IY48vzpxxIxnhgU-8_X8iBdprwrxxi1ipQlW03wTsdQJxsuQXEFAlLoji4GDxcNwTg6HCiuazvL7z2O9PNjl8fh2ZqRUJ-o8-S6h_YDJS_h3S0DlXKqkOT7D3ySid1lnkl4pnGfH3UeTRWR8sIsFFiXZJG9XbDSN9gE4zaC8hZ0jSkn0PtpXjhmQud319eMzWMp1Mlvnzs-zLMPg1csdetR4byz5kNwCcq2aUTB_ZxUjs12GbwXpFRQn_vEU_V7dkngDEVgaLf40fI1C5tq-0sXk5z_JfZuJ-YnChFW20um7CboWuRyQgWfZD5J2YpKXa6o_N4uTl6AQhcif_0sROuGY5TRw4uxC_Y9i0R8-bZ8zytLX7R6atuqXTnRhDI-cY9jVQkxwEgDadLUuYMA=w453-h805-no)

[Here](http://www.rabbitlaserusa.com/manuals/MPC6515HardwareManual.pdf) the hardware manual of the laser cutter

[Here](https://drive.google.com/file/d/0B4KNW3XBN0r0WHJ2bXZvNFVPemM/view?usp=sharing) the chart of the code
