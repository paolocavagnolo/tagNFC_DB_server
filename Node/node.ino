//General
#include <SPI.h>

//NFC side
#include <Wire.h>
#include <Adafruit_PN532.h>

//RFM side
#include <RFM69.h>        //get it here: https://www.github.com/lowpowerlab/rfm69
#include <RFM69_ATC.h>    //get it here: https://www.github.com/lowpowerlab/rfm69
#include <SPIFlash.h>     //get it here: https://www.github.com/lowpowerlab/spiflash


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
//#define IS_RFM69HW    //uncomment only for RFM69HW! Leave out if you have RFM69W!
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
byte sendSize=0;
boolean requestACK = false;

//Flash side
SPIFlash flash(FLASH_SS, 0xEF30); //EF30 for 4mbit  Windbond chip (W25X40CL)

#ifdef ENABLE_ATC
  RFM69_ATC radio;
#else
  RFM69 radio;
#endif

void setup() {
  Serial.begin(SERIAL_BAUD);

  //NFC side
  nfc.begin();
  uint32_t versiondata = nfc.getFirmwareVersion();
  if (! versiondata) {
    Serial.print("Didn't find PN53x board");
    while (1); // halt
  }
  Serial.print("Found chip PN5"); Serial.println((versiondata>>24) & 0xFF, HEX);
  Serial.print("Firmware ver. "); Serial.print((versiondata>>16) & 0xFF, DEC);
  Serial.print('.'); Serial.println((versiondata>>8) & 0xFF, DEC);

  // configure board to read RFID tags
  nfc.SAMConfig();

  Serial.println("Waiting for an ISO14443A Card ...");

  //RFM side
  radio.initialize(FREQUENCY,NODEID,NETWORKID);
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
  sprintf(buff, "\nTransmitting at %d Mhz...", FREQUENCY==RF69_433MHZ ? 433 : FREQUENCY==RF69_868MHZ ? 868 : 915);
  Serial.println(buff);

  if (flash.initialize())
  {
    Serial.print("SPI Flash Init OK ... UniqueID (MAC): ");
    flash.readUniqueId();
    for (byte i=0;i<8;i++)
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
}

void Blink(byte PIN, int DELAY_MS)
{
  pinMode(PIN, OUTPUT);
  digitalWrite(PIN,HIGH);
  delay(DELAY_MS);
  digitalWrite(PIN,LOW);
}

long lastPeriod = 0;
bool LuceEnable = false;
bool LaserOn = false;
//NFC side
uint8_t success;
uint8_t uid[] = { 0, 0, 0, 0, 0, 0, 0 };  // Buffer to store the returned UID
uint8_t uidLength;                        // Length of the UID (4 or 7 bytes depending on ISO14443A card type)


void loop() {

  if (!LuceEnable) {
    success = nfc.readPassiveTargetID(PN532_MIFARE_ISO14443A, uid, &sendSize);
    if (success) {
      // Display some basic information about the card
      Serial.println("Found an ISO14443A card");
      Serial.print("  UID Length: ");Serial.print(uidLength, DEC);Serial.println(" bytes");
      Serial.print("  UID Value: ");
      nfc.PrintHex(uid, uidLength);
    }

    //Ascolta il gateway per l'ok
    delay(1000);
    LuceEnable = true;
    delay(1000);
    LuceEnable = false;
    // if (radio.receiveDone())
    // {
    //   Serial.print('[');Serial.print(radio.SENDERID, DEC);Serial.print("] ");
    //   for (byte i = 0; i < radio.DATALEN; i++)
    //     Serial.print((char)radio.DATA[i]);
    //   Serial.print("   [RX_RSSI:");Serial.print(radio.RSSI);Serial.print("]");
    //
    //   if (radio.ACKRequested())
    //   {
    //     radio.sendACK();
    //     Serial.print(" - ACK sent");
    //   }
    //   Blink(LED,3);
    //   Serial.println();
    // }

    //Manda
    int currPeriod = millis()/TRANSMITPERIOD;
    if (currPeriod != lastPeriod)
    {
      lastPeriod=currPeriod;

      sprintf(buff, "FLASH_MEM_ID:0x%X", flash.readDeviceId());
      byte buffLen=strlen(buff);
      if (radio.sendWithRetry(GATEWAYID, buff, buffLen))
        Serial.print(" ok!");
      else Serial.print(" nothing...");

      Serial.print("Sending[");
      Serial.print(sendSize);
      Serial.print("]: ");

      if (radio.sendWithRetry(GATEWAYID, uid, sendSize))
       Serial.print(" ok!");
      else Serial.print(" nothing...");

      Serial.println();
      Blink(LED,3);
    }

  }

  //READ TIME LASER

  // while (analogRead(0)>1000) {
  //   if (LaserOn) {
  //     inizio = millis();
  //     LaserOn = true;    //inizia a contare il tempo
  //   }
  //   if ((millis() - inizio) > Cr_time) {
  //     scala_cr(tagId_OK,tagId_NO);
  //     inizio = millis();
  //   }
  // }
  // if (flagLaser==true) {
  //   fine = millis();
  //   flagLaser=false;
  //   durata += abs(fine - inizio);
  //
  //   if (durata > Cr_time) {
  //     scala_cr(tagId_OK,tagId_NO);//scala
  //     durata = 0;
  //   }
  // }

  //gestisci l'abilitazione del laser
  // if (flag_enable == true) {    //se ti è arrivato il segnale di abilitazione
  //   digitalWrite(enable,HIGH); //abilita il laser
  //   digitalWrite(ledOK,HIGH);  //accende il led verde
  // }
  // else {
  //   digitalWrite(enable,LOW);
  //   digitalWrite(ledOK,LOW);
  // }
  //
  // if (flag_danger == true) {
  //   digitalWrite(ledNO,HIGH);  //accende il led verde
  // }
  // else {
  //   digitalWrite(ledNO,LOW);
  // }

  //TIME OUT
  //
  // if (flagLaser==true) {
  //   fine = millis();
  //   flagLaser=false;
  //   durata += abs(fine - inizio);
  //
  //   if (durata > Cr_time) {
  //     scala_cr(tagId_OK,tagId_NO);//scala
  //     durata = 0;
  //   }
  // }

}
