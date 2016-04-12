# tagNFC_DB_server

An open source system to manage machines in a cool makerspace!

The system is composed by nodes and 1 gateway. The gateway is a arduino YUN with an RFM69 moteino board.
Each node has at least 1 moteino board and a NFC tag shield.

## Gateway

I'm using Raspberry PI 3.
Download raspbian from [here] (https://www.raspberrypi.org/downloads/raspbian/)

Follow all the instructions [here](https://www.raspberrypi.org/documentation/installation/installing-images/)

Check for the UART communication

      Hi,
      First of all, thanks for the information. My serial connection has started to work!
      I've added core_freq=250 to /boot/config.txt on my Pi 3.
      vcgencmd get_config arm_freq reports 1200 and /sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq shows 600000 and 1200000. It looks like performance of the board didn't decrease.
      Of course I use /dev/ttyS0 device.

Install pySerial

      sudo apt-get install python-serial

and then

      import serial

      port = serial.Serial("/dev/ttyAMA0", baudrate=115200, timeout=3.0)

      while True:
        port.write("\r\nSay something:")
        rcv = port.read(10)
        port.write("\r\nYou sent:" + repr(rcv))

## Laser node
###Hacking the Laser
![Alt text](https://lh3.googleusercontent.com/XCoaaOT6O4BzO5U8wtSX5OgKLz_5uHQfqf0ip7A4G7SFzWbD5I9IVt8VVpTohM7vxBachwNntntgR7AXrMmXbZT2xcmWbJHFiKCxw51UEXsCrnUGEzItq08hpOqjPtaAMyVmiOfyLbpttHSsaZAfdHApaE0IhWU2CuKlxmATBdZQVPPnSq5IY48vzpxxIxnhgU-8_X8iBdprwrxxi1ipQlW03wTsdQJxsuQXEFAlLoji4GDxcNwTg6HCiuazvL7z2O9PNjl8fh2ZqRUJ-o8-S6h_YDJS_h3S0DlXKqkOT7D3ySid1lnkl4pnGfH3UeTRWR8sIsFFiXZJG9XbDSN9gE4zaC8hZ0jSkn0PtpXjhmQud319eMzWMp1Mlvnzs-zLMPg1csdetR4byz5kNwCcq2aUTB_ZxUjs12GbwXpFRQn_vEU_V7dkngDEVgaLf40fI1C5tq-0sXk5z_JfZuJ-YnChFW20um7CboWuRyQgWfZD5J2YpKXa6o_N4uTl6AQhcif_0sROuGY5TRw4uxC_Y9i0R8-bZ8zytLX7R6atuqXTnRhDI-cY9jVQkxwEgDadLUuYMA=w453-h805-no)

[Here](http://www.rabbitlaserusa.com/manuals/MPC6515HardwareManual.pdf) the hardware manual of the laser cutter

[Here](https://drive.google.com/file/d/0B4KNW3XBN0r0WHJ2bXZvNFVPemM/view?usp=sharing) the chart of the code
