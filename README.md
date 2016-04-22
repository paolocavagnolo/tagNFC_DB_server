# tagNFC_DB_server

An open source system to manage machines in a cool makerspace!

The system is composed by nodes and 1 gateway. The gateway is a raspberry pi 3 with an RFM69 moteino board connected trough UART.
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

## Set-up github on local machine

      sudo apt-get install git-core
      ssh-keygen -t rsa -b 4096 -C "you@example.com"
      eval "$(ssh-agent -s)"
      ssh-add ~/.ssh/id_rsa
      tail ~/.ssh/id_rsa.pub
      --copy and paste it to github/settings--
      git clone git@github.com:paolocavagnolo/tagNFC_DB_server.git
      git config --global user.email "you@example.com"
      git config --global user.name "Your Name"



      


## Set-up VPN for remote controll

https://www.digitalocean.com/community/tutorials/how-to-set-up-an-openvpn-server-on-debian-8

## Platformio

http://www.russelldavis.org/2015/08/01/platformio-on-the-raspberry-pi/

      sudo apt-get install libmpc-dev libelf1 libftdi1
