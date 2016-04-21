///General
#include <SPI.h>

//Timer 1
#include <avr/io.h>
#include <avr/interrupt.h>

//NFC side
#include <Wire.h>
#include <Adafruit_PN532.h>

//RFM side
#include <RFM69.h>
#include <RFM69_ATC.h>
#include <SPIFlash.h>

//Display side
#include "LedControl.h"

///NFC side
#define PN532_IRQ   (3)
#define PN532_RESET (4)
Adafruit_PN532 nfc(PN532_IRQ, PN532_RESET);

//RFM side
#define NODEID        2
#define NETWORKID     100
#define GATEWAYID     1
#define FREQUENCY   RF69_433MHZ
#define ENCRYPTKEY    "sampleEncryptKey"
#define IS_RFM69HW
#define ENABLE_ATC

#ifdef ENABLE_ATC
RFM69_ATC radio;
#else
RFM69 radio;
#endif

byte sendSize = 0;
boolean requestACK = false;

//HARDWARE side
#define LED           9 // Moteinos have LEDs on D9
#define FLASH_SS      8 // and FLASH SS on D8
#define SERIAL_BAUD   115200

//7Segment side
LedControl lc = LedControl(17, 16, 15, 1);

//Flash side
SPIFlash flash(FLASH_SS, 0xEF30);

//Sicurity side
uint8_t CheckTresh = 0;

void setup() {
  pinMode(5, OUTPUT);   //Red
  pinMode(6, OUTPUT);   //Green
  pinMode(7, OUTPUT);

  Serial.begin(SERIAL_BAUD);

  //Timer1
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
  byte zero[] = {'0', '0', '0', '0', '0', '0', '0', '0'};
  //Sync CheckTreshold
  sendToGateway('k', zero);
  long timeOutAnswer = millis();
  while ((!radio.receiveDone()) && (millis() - timeOutAnswer) < 10000) {}
  if (radio.receiveDone()) {
    CheckTresh = radio.DATA[2];
    Serial.println("Synced Check Treshold");
  }
  else {
    Serial.println("NO RADIO CONNECTION WITH GATEWAY");
  }

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
    if ((millis() - trigTime) > (2023 - ar)) {
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


long lastPeriod = 0;

bool readEnable = false;
bool laserEnable = false;

//NFC side
uint8_t success;
uint8_t uid[] = {0, 0, 0, 0, 0, 0, 0, 0};  // Buffer to store the returned UID
byte uidLength = 0;

byte MessageToGateway[] = {'<', '0', '0', 'a', '1', '2', '3', '4', '5', '6', '7', '8', '>'};
byte TypeFromGateway;
byte MessageFromGateway[] = {'0', '0', '0', '0', '0', '0', '0', '0'};

float Cr = 0;
int Sk = 0;
bool timeout = false;

union u_Cr {
  byte b[4];
  float fval;
} u;

void loop() {
  //debug
  Serial.println("Beginning of the loop - initialize the variables");

  //initialize variables at reset or timeout
  digitalWrite(7, LOW);
  readEnable = false;
  laserEnable = false;
  timeout = false;

  if (!readEnable) {
    //read tag
    success = nfc.readPassiveTargetID(PN532_MIFARE_ISO14443A, uid, &uidLength);
    if (success) {
      // Display some basic information about the card
      Serial.println("Found an ISO14443A card");
      Serial.print("  UID Length: "); Serial.print(sendSize, DEC); Serial.println(" bytes");
      Serial.print("  UID Value: ");
      nfc.PrintHex(uid, uidLength);
      //display it
      setDisplay(uid);
      //send to gateway
      if (sendToGateway('n', uid)) {
        Serial.println("TagID to gateway sent and ACK ok! :)");
      }
      else Serial.println("TagID to gateway sent and but no ACK :(");
      //check answer
      switch (answerFromGateway(10000)) {
        case 'z': //crack
          Serial.println("Error in check treshold of incremental number **POSSIBLE ATTACK!**");
          break;
        case 't': //timeout
          Serial.println("Time out recieving answer after TagID sent");
          break;
        case 'a':
          switch (TypeFromGateway) {
            case 'r':
              if (MessageToGateway[0] > 0) {
                for (int i = 0; i < 4; i++) u.b[i] = MessageToGateway[i];
                Cr = u.fval;
                Sk = MessageToGateway[3];
                laserEnable = true;
              }
              else {
                //No tagID:
                Serial.println("No Person Found");
                Blink(5, 500);
              }
              break;

            case 'd':
              Serial.println("door open?! in the laser?");
              break;
          }
          break;
      }
    } // close read tag

    while (laserEnable) {
      if (Cr > 0) {
        digitalWrite(7, HIGH);
      }
      printCr(Cr, Sk);
      digitalWrite(6, HIGH);
      long iTimeOut = millis();
      while (!timeout) {
        if (tick > 10) {
          iTimeOut = millis();
          if (sendToGateway('l', uid)) {
            Serial.println("Tick to gateway sent and ACK ok! :)");
          }
          else Serial.println("Tick to gateway sent and but no ACK :(");
          tick -= 10;

          switch (answerFromGateway(10000)) {
            case 'z': //crack
              Serial.println("Error in check treshold of incremental number **POSSIBLE ATTACK!**");
              break;
            case 't': //timeout
              Serial.println("Time out recieving answer after TagID sent");
              break;
            case 'a':
              switch (TypeFromGateway) {
                case 'r':
                  if (MessageToGateway[0] > 0) {
                    for (int i = 0; i < 4; i++) u.b[i] = MessageToGateway[i];
                    Cr = u.fval;
                    Sk = MessageToGateway[3];
                    printCr(Cr, Sk);
                  }
                  else {
                    //No tagID:
                    Serial.println("No Person Found");
                    Blink(5, 500);
                  }
                  break;

                case 'd':
                  Serial.println("door open?! in the laser?");
                  break;
              }
              break;
          }
        }
        if ((millis() - iTimeOut) > 300000) {
          timeout = true;
        }

      }
    }

  }

} //close loop

int sendToGateway(char type, byte message[8]) {
  MessageToGateway[0] = '<';       //SoC
  MessageToGateway[1] = NODEID;    //Node ID
  CheckTresh++;
  if (CheckTresh > 254) {
    CheckTresh = 0;
  }
  MessageToGateway[2] = (char)(CheckTresh);  //Security incremental
  MessageToGateway[3] = type;
  for (int i = 0; i < 8; i++) MessageToGateway[4 + i] = message[i];
  MessageToGateway[12] = '>';

  return radio.sendWithRetry(GATEWAYID, MessageToGateway, 13);

}

char answerFromGateway(long timeOut) {
  long timeOutAnswer = millis();
  while ((!radio.receiveDone()) && (millis() - timeOutAnswer) < timeOut) {}
  if (radio.receiveDone()) {
    //Check incremental variable
    if (radio.DATA[2] > CheckTresh) {
      CheckTresh + 1;
    }
    else {
      return 'z';
    }
    TypeFromGateway = radio.DATA[3];
    for (int i = 0; i < 8; i++) MessageFromGateway[i] = radio.DATA[4 + i];
    return 'a';
  }
  else return 't';
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

void printCr(float number, int sk) {
  uint8_t ones, tens, hundreds, dec;

  hundreds = number / 100;
  number = number - hundreds * 100;

  tens = number / 10;
  ones = number - tens * 10;
  number = number - tens * 10;
  dec = (number - ones) * 10;


  lc.clearDisplay(0);
  if (sk == 0) {
    lc.setChar(0, 7, 'b', false);
  }
  else {
    lc.setChar(0, 7, 'A', false);
  }
  lc.setDigit(0, 3, hundreds, false);
  lc.setDigit(0, 2, tens, false);
  lc.setDigit(0, 1, ones, true);
  lc.setDigit(0, 0, dec, false);
}
