#include <SPI.h>
#include <avr/io.h>
#include <avr/interrupt.h>
#include <Wire.h>
#include <Adafruit_PN532.h>
#include <RFM69.h>        //get it here: https://www.github.com/lowpowerlab/rfm69
#include <RFM69_ATC.h>    //get it here: https://www.github.com/lowpowerlab/rfm69
#include <SPIFlash.h>     //get it here: https://www.github.com/lowpowerlab/spiflash
#include <LedControl.h>

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
#define FREQUENCY   RF69_433MHZ
#define ENCRYPTKEY    "sampleEncryptKey" //exactly the same 16 characters/bytes on all nodes!
#define IS_RFM69HW    //uncomment only for RFM69HW! Leave out if you have RFM69W!
#define ENABLE_ATC    //comment out this line to disable AUTO TRANSMISSION CONTROL
#define SERIAL_BAUD   115200
//pinout
#define LED           9 // Moteinos have LEDs on D9
#define FLASH_SS      8 // and FLASH SS on D8
//*********************************************************************************************

byte sendSize = 0;
boolean requestACK = false;

//7Segment side
LedControl lc = LedControl(17, 16, 15, 1);

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

  Serial.begin(SERIAL_BAUD);

  cli();
  TCCR1A = 0;
  TCCR1B = 0;
  TIMSK1 = (1 << TOIE1);
  TCCR1B |= (1 << CS11);
  sei();

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
  lc.shutdown(0, false);
  lc.setIntensity(0, 8);
  lc.clearDisplay(0);

}

volatile long trigTime = 0;
int ar = 0;
long tick = 0;
bool trig = false;

ISR(TIMER1_OVF_vect)
{
  ar = analogRead(0);
  if (ar > 15) {
    if (!trig) trigTime = millis();
    trig = true;
    if ((millis() - trigTime) > (2023-ar)) {
      tick++;
      trigTime = 0;
      trig = false;
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

long lastPeriod = 0;
bool readEnable = false;
bool LaserOn = false;
//NFC side
uint8_t success;
uint8_t uid[] = { 0, 0, 0, 0, 0, 0, 0, 0 };  // Buffer to store the returned UID

uint8_t uidLength;                        // Length of the UID (4 or 7 bytes depending on ISO14443A card type)
bool ansCr = false;
bool ansSk = false;
bool answered = false;
bool answered2 = false;
char tagLife = ' ';
String mode = "";
int Cr = 0;
int Sk = 0;
bool timeout = false;

void loop() {

  //laser off
  digitalWrite(7, LOW);
  readEnable = true;
  answered = false;
  answered2 = false;
  timeout = false;

  if (readEnable) {
    //read tag
    success = nfc.readPassiveTargetID(PN532_MIFARE_ISO14443A, uid, &sendSize);
    if (success) {
      // Display some basic information about the card
      Serial.println("Found an ISO14443A card");
      Serial.print("  UID Length: "); Serial.print(sendSize, DEC); Serial.println(" bytes");
      Serial.print("  UID Value: ");
      for (int i=0; i<(int)sendSize-1; i++) {
          uid[i] = uid[i+1];
      }
      nfc.PrintHex(uid, sendSize-1);
      //send to gateway
      if (radio.sendWithRetry(GATEWAYID, uid, sendSize)) {
        Serial.print(" ok!");
      }
      else Serial.print(" nothing...");
      //display
      setDisplay(uid);
    }
    readEnable = false;
  }
  //end loop

}

String hexify(unsigned int n)
{
  String res;

  do
  {
    res += "0123456789ABCDEF"[n % 16];
    n >>= 4;
  } while (n);

  return res;
}

void setDisplay(uint8_t id[]) {
  lc.setChar(0, 7, hexify(id[0])[1], false);
  lc.setChar(0, 6, hexify(id[0])[0], false);
  lc.setChar(0, 5, hexify(id[1])[1], false);
  lc.setChar(0, 4, hexify(id[1])[0], false);
  lc.setChar(0, 3, hexify(id[2])[1], false);
  lc.setChar(0, 2, hexify(id[2])[0], false);
  lc.setChar(0, 1, hexify(id[3])[1], false);
  lc.setChar(0, 0, hexify(id[3])[0], false);
}

void printCr(int number, int sk) {
  uint8_t ones, tens, hundreds;

  hundreds = number / 100;
  number = number - hundreds * 100;

  tens = number / 10;
  ones = number - tens * 10;

  lc.clearDisplay(0);
  if (sk == 0) {
    lc.setChar(0, 7, 'b', false);
  }
  else {
    lc.setChar(0, 7, 'A', false);
  }
  lc.setDigit(0, 2, hundreds, false);
  lc.setDigit(0, 1, tens, false);
  lc.setDigit(0, 0, ones, false);
}
