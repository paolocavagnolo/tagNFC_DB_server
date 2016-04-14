//General
#include <SPI.h>

//NFC side
#include <Wire.h>
#include <Adafruit_PN532.h>

//RFM side
#include <RFM69.h>        //get it here: https://www.github.com/lowpowerlab/rfm69
#include <RFM69_ATC.h>    //get it here: https://www.github.com/lowpowerlab/rfm69
#include <SPIFlash.h>     //get it here: https://www.github.com/lowpowerlab/spiflash

//7Segment side
#include "LedControl.h"

//*********************************************************************************************
//************ IMPORTANT SETTINGS - YOU MUST CHANGE/CONFIGURE TO FIT YOUR HARDWARE *************
//*********************************************************************************************
//NFC side
#define PN532_IRQ   (3)
#define PN532_RESET (4)

Adafruit_PN532 nfc(PN532_IRQ, PN532_RESET);

//RFM side
#define NODEID        2    //must be unique for each node on same network (range up to 254, 255 is used for broadcast)
#define NETWORKID     100  //the same on all nodes that talk to each other (range up to 255)
#define GATEWAYID     1
//Match frequency to the hardware version of the radio on your Moteino (uncomment one):
#define FREQUENCY   RF69_433MHZ
//#define FREQUENCY   RF69_868MHZ
//#define FREQUENCY     RF69_915MHZ
#define ENCRYPTKEY    "sampleEncryptKey" //exactly the same 16 characters/bytes on all nodes!
#define IS_RFM69HW    //uncomment only for RFM69HW! Leave out if you have RFM69W!
#define ENABLE_ATC    //comment out this line to disable AUTO TRANSMISSION CONTROL
//*********************************************************************************************

#ifdef __AVR_ATmega1284P__
#define LED           15 // Moteino MEGAs have LEDs on D15
#define FLASH_SS      23 // and FLASH SS on D23
#else
#define LED           9 // Moteinos have LEDs on D9
#define FLASH_SS      8 // and FLASH SS on D8
#endif

#define SERIAL_BAUD   115200

int TRANSMITPERIOD = 150; //transmit a packet to gateway so often (in ms)
char payload[] = "";
char buff[20];
byte sendSize = 0;
boolean requestACK = false;

//7Segment side
LedControl lc = LedControl(17,16,15,1);

//Flash side
SPIFlash flash(FLASH_SS, 0xEF30); //EF30 for 4mbit  Windbond chip (W25X40CL)

#ifdef ENABLE_ATC
RFM69_ATC radio;
#else
RFM69 radio;
#endif

void setup() {
  pinMode(5, OUTPUT);
  pinMode(6, OUTPUT);
  pinMode(7, OUTPUT);
  digitalWrite(7, HIGH);

  Serial.begin(SERIAL_BAUD);

  //NFC side
  nfc.begin();
  uint32_t versiondata = nfc.getFirmwareVersion();
  if (! versiondata) {
    Serial.print("Didn't find PN53x board");
    while (1); // halt
  }
  Serial.print("Found chip PN5"); Serial.println((versiondata >> 24) & 0xFF, HEX);
  Serial.print("Firmware ver. "); Serial.print((versiondata >> 16) & 0xFF, DEC);
  Serial.print('.'); Serial.println((versiondata >> 8) & 0xFF, DEC);

  // configure board to read RFID tags
  nfc.SAMConfig();

  Serial.println("Waiting for an ISO14443A Card ...");

  //RFM side
  radio.initialize(FREQUENCY, NODEID, NETWORKID);
#ifdef IS_RFM69HW
  radio.setHighPower(); //uncomment only for RFM69HW!
#endif
  radio.encrypt(ENCRYPTKEY);
  //radio.setFrequency(919000000); //set frequency to some custom frequency

  //Auto Transmission Control - dials down transmit power to save battery (-100 is the noise floor, -90 is still pretty good)
  //For indoor nodes that are pretty static and at pretty stable temperatures (like a MotionMote) -90dBm is quite safe
  //For more variable nodes that can expect to move or experience larger temp drifts a lower margin like -70 to -80 would probably be better
  //Always test your ATC mote in the edge cases in your own environment to ensure ATC will perform as you expect
#ifdef ENABLE_ATC
  radio.enableAutoPower(-70);
#endif

  char buff[50];
  sprintf(buff, "\nTransmitting at %d Mhz...", FREQUENCY == RF69_433MHZ ? 433 : FREQUENCY == RF69_868MHZ ? 868 : 915);
  Serial.println(buff);

  if (flash.initialize())
  {
    Serial.print("SPI Flash Init OK ... UniqueID (MAC): ");
    flash.readUniqueId();
    for (byte i = 0; i < 8; i++)
    {
      Serial.print(flash.UNIQUEID[i], HEX);
      Serial.print(' ');
    }
    Serial.println();
  }
  else
    Serial.println("SPI Flash MEM not found (is chip soldered?)...");

#ifdef ENABLE_ATC
  Serial.println("RFM69_ATC Enabled (Auto Transmission Control)\n");
#endif

//7Segment side
lc.shutdown(0,false);
lc.setIntensity(0,8);
lc.clearDisplay(0);

}

void Blink(byte PIN, int DELAY_MS)
{
  pinMode(PIN, OUTPUT);
  digitalWrite(PIN, HIGH);
  delay(DELAY_MS);
  digitalWrite(PIN, LOW);
}

String hexify(unsigned int n)
{
  String res;

  do
  {
    res += "0123456789ABCDEF"[n % 16];
    n >>= 4;
  } while(n);

  return res;
}


long lastPeriod = 0;
bool LuceEnable = false;
bool LaserOn = false;
//NFC side
uint8_t success;
uint8_t uid[] = { 0, 0, 0, 0, 0, 0, 0 };  // Buffer to store the returned UID
uint8_t uidLength;                        // Length of the UID (4 or 7 bytes depending on ISO14443A card type)


void loop() {

  //ACK Gateway
  //send an ACK
  if (radio.ACKRequested())
  {
    radio.sendACK();
    Serial.print(" - ACK sent");
  }

  if (!LuceEnable) {
    success = nfc.readPassiveTargetID(PN532_MIFARE_ISO14443A, uid, &sendSize);
    if (success) {
      // Display some basic information about the card
      Serial.println("Found an ISO14443A card");
      Serial.print("  UID Length: "); Serial.print(sendSize, DEC); Serial.println(" bytes");
      Serial.print("  UID Value: ");
      nfc.PrintHex(uid, sendSize);
      lc.setChar(0,7,hexify(uid[0])[0],false);
      lc.setChar(0,6,hexify(uid[0])[1],false);
      lc.setChar(0,5,hexify(uid[1])[0],false);
      lc.setChar(0,4,hexify(uid[1])[1],false);
      lc.setChar(0,3,hexify(uid[2])[0],false);
      lc.setChar(0,2,hexify(uid[2])[1],false);
      lc.setChar(0,1,hexify(uid[3])[0],false);
      lc.setChar(0,0,hexify(uid[3])[1],false);

    }
    //Li



    LuceEnable = true;
  }


  //trasmetti
  if (radio.sendWithRetry(GATEWAYID, uid, sendSize)) {
    Serial.print(" ok!");
  }
  else Serial.print(" nothing...");
  }
  Blink(LED, 3);


}
