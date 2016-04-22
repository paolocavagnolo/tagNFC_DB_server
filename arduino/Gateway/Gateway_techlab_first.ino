// Sample RFM69 receiver/gateway sketch, with ACK and optional encryption, and Automatic Transmission Control
// Passes through any wireless received messages to the serial port & responds to ACKs
// It also looks for an onboard FLASH chip, if present
// RFM69 library and sample code by Felix Rusu - http://LowPowerLab.com/contact
// Copyright Felix Rusu (2015)

#include <RFM69.h>    //get it here: https://www.github.com/lowpowerlab/rfm69
#include <RFM69_ATC.h>//get it here: https://www.github.com/lowpowerlab/rfm69
#include <SPI.h>      //comes with Arduino IDE (www.arduino.cc)
#include <SPIFlash.h> //get it here: https://www.github.com/lowpowerlab/spiflash

//*********************************************************************************************
//************ IMPORTANT SETTINGS - YOU MUST CHANGE/CONFIGURE TO FIT YOUR HARDWARE *************
//*********************************************************************************************
#define NODEID        1    //unique for each node on same network
#define LASERID       2
#define NETWORKID     100  //the same on all nodes that talk to each other
//Match frequency to the hardware version of the radio on your Moteino (uncomment one):
#define FREQUENCY     RF69_433MHZ
//#define FREQUENCY     RF69_868MHZ
//#define FREQUENCY     RF69_915MHZ
#define ENCRYPTKEY    "sampleEncryptKey" //exactly the same 16 characters/bytes on all nodes!
#define IS_RFM69HW    //uncomment only for RFM69HW! Leave out if you have RFM69W!
#define ENABLE_ATC    //comment out this line to disable AUTO TRANSMISSION CONTROL
//*********************************************************************************************

#define SERIAL_BAUD   115200

#ifdef __AVR_ATmega1284P__
#define LED           15 // Moteino MEGAs have LEDs on D15
#define FLASH_SS      23 // and FLASH SS on D23
#else
#define LED           9 // Moteinos have LEDs on D9
#define FLASH_SS      8 // and FLASH SS on D8
#endif

#ifdef ENABLE_ATC
RFM69_ATC radio;
#else
RFM69 radio;
#endif

SPIFlash flash(FLASH_SS, 0xEF30); //EF30 for 4mbit  Windbond chip (W25X40CL)
bool promiscuousMode = false; //set to 'true' to sniff all packets on the same network

void setup() {
  Serial.begin(SERIAL_BAUD);
  delay(10);
  radio.initialize(FREQUENCY, NODEID, NETWORKID);
#ifdef IS_RFM69HW
  radio.setHighPower(); //only for RFM69HW!
#endif
  radio.encrypt(ENCRYPTKEY);
  radio.promiscuous(promiscuousMode);
  //radio.setFrequency(919000000); //set frequency to some custom frequency
  char buff[50];
  sprintf(buff, "\nListening at %d Mhz...", FREQUENCY == RF69_433MHZ ? 433 : FREQUENCY == RF69_868MHZ ? 868 : 915);
  Serial.println(buff);
  if (flash.initialize())
  {
    Serial.print("SPI Flash Init OK. Unique MAC = [");
    flash.readUniqueId();
    for (byte i = 0; i < 8; i++)
    {
      Serial.print(flash.UNIQUEID[i], HEX);
      if (i != 8) Serial.print(':');
    }
    Serial.println(']');

    //alternative way to read it:
    //byte* MAC = flash.readUniqueId();
    //for (byte i=0;i<8;i++)
    //{
    //  Serial.print(MAC[i], HEX);
    //  Serial.print(' ');
    //}
  }
  else
    Serial.println("SPI Flash MEM not found (is chip soldered?)...");

#ifdef ENABLE_ATC
  Serial.println("RFM69_ATC Enabled (Auto Transmission Control)");
#endif
}

byte ackCount = 0;
uint32_t packetCount = 0;
uint8_t dataRecevied[7];
int Cr = 0; //credits
int Ab = 0; //abilitation code
byte incomingByte[5];
char feedback[4];
byte nodeID;
byte sendSize = 1;

void loop() {

  //process any serial input
  if (Serial.available() > 0)
  {
    char input = Serial.read();
    if (input == 'n') //new tag
    {
      feedback[0] = 'n';
      Serial.println("GGW: New tag found!");
      radio.sendWithRetry(LASERID, feedback, 1);
    }
    else if (input == 'c') //new tag
    {
      feedback[0] = 'c';
      Serial.println("GGW: Person! credits..");
      feedback[1] = (char)Serial.read();
      radio.sendWithRetry(LASERID, feedback, 2);
    }
    else if (input == 's') //new tag
    {
      feedback[0] = 's';
      Serial.println("GGW: Person! skills..");
      feedback[1] = (char)Serial.read();
      radio.sendWithRetry(LASERID, feedback, 2);
    }
  }

  if (radio.receiveDone())
  {
    for (byte i = 0; i < radio.DATALEN; i++)
      dataRecevied[i] = radio.DATA[i];

    if (dataRecevied[0] == '-') {
      Serial.print("-tick");
    }
    else {

      Serial.print("#,");
      Serial.print(++packetCount);
      Serial.print(',');
      Serial.print(','); Serial.print(radio.SENDERID, DEC); Serial.print(",");
      nodeID = radio.SENDERID;

      PrintHex8(dataRecevied, 7);
      Serial.print(",RX_RSSI:"); Serial.print(radio.RSSI); Serial.print(",");
    }
    if (radio.ACKRequested())
    {
      byte theNodeID = radio.SENDERID;
      radio.sendACK();
      Serial.print("ACK sent,");

      Serial.println();
      Blink(LED, 3);
    }
  }
}

void Blink(byte PIN, int DELAY_MS)
{
  pinMode(PIN, OUTPUT);
  digitalWrite(PIN, HIGH);
  delay(DELAY_MS);
  digitalWrite(PIN, LOW);
}

void PrintHex8(uint8_t *data, uint8_t length) // prints 8-bit data in hex
{
  char tmp[length * 5 + 1];
  byte first;
  byte second;
  for (int i = 0; i < length; i++) {
    first = (data[i] >> 4) & 0x0f;
    second = data[i] & 0x0f;
    // base for converting single digit numbers to ASCII is 48
    // base for 10-16 to become upper-case characters A-F is 55
    // note: difference is 7
    tmp[i * 5] = 48; // add leading 0
    tmp[i * 5 + 1] = 120; // add leading x
    tmp[i * 5 + 2] = first + 48;
    tmp[i * 5 + 3] = second + 48;
    tmp[i * 5 + 4] = 32; // add trailing space
    if (first > 9) tmp[i * 5 + 2] += 7;
    if (second > 9) tmp[i * 5 + 3] += 7;
  }
  tmp[length * 5] = 0;
  Serial.print(tmp);
}
