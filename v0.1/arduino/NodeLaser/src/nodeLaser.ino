#include <SPI.h>
#include <avr/io.h>
#include <avr/interrupt.h>
#include <Wire.h>
#include <Adafruit_PN532.h>
#include <RFM69.h>        //get it here: https://www.github.com/lowpowerlab/rfm69
#include <RFM69_ATC.h>    //get it here: https://www.github.com/lowpowerlab/rfm69
#include <SPIFlash.h>     //get it here: https://www.github.com/lowpowerlab/spiflash
#include <LedControl.h>

//**********************************************************************************************
//************ IMPORTANT SETTINGS - YOU MUST CHANGE/CONFIGURE TO FIT YOUR HARDWARE *************
//*********************************************************************************************+

//NFC side
#define PN532_IRQ   (3)
#define PN532_RESET (4)
Adafruit_PN532 nfc(PN532_IRQ, PN532_RESET);

//RFM side
#define NODEID        2    //must be unique for each node on same network (range up to 254, 255 is used for broadcast)
#define NETWORKID     100  //the same on all nodes that talk to each other (range up to 255)
#define GATEWAYID     1
#define FREQUENCY     RF69_433MHZ
#define ENCRYPTKEY    "sampleEncryptKey" //exactly the same 16 characters/bytes on all nodes!
#define IS_RFM69HW    //uncomment only for RFM69HW! Leave out if you have RFM69W!
#define ENABLE_ATC    //comment out this line to disable AUTO TRANSMISSION CONTROL
#define SERIAL_BAUD   115200

//pinout
#define LED           9 // Moteinos have LEDs on D9
#define RED           5 // Led
#define GREEN         6 // Led
#define LASER         7 // Relay
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
  pinMode(RED, OUTPUT);
  pinMode(GREEN, OUTPUT);
  pinMode(LASER, OUTPUT);

  Serial.begin(SERIAL_BAUD);

  noInterrupts(); // disable all interrupts
  TCCR1A = 0;
  TCCR1B = 0;
  TCNT1 = 0;

  OCR1A = 6250; // compare match register 16MHz/256/10Hz
  TCCR1B |= (1 << WGM12); // CTC mode
  TCCR1B |= (1 << CS12); // 256 prescaler
  TIMSK1 |= (1 << OCIE1A); // enable timer compare interrupt
  interrupts(); // enable all interrupts

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

volatile float trigTime = 0;
float ar = 0;

ISR(TIMER1_COMPA_vect)
{
  ar = analogRead(0);
  if (ar > 100) {
    trigTime = trigTime + (ar / 1500) + 0.318;
  }
}

void Blink(byte PIN, int DELAY_MS)
{
  pinMode(PIN, OUTPUT);
  digitalWrite(PIN, HIGH);
  delay(DELAY_MS);
  digitalWrite(PIN, LOW);
}

float bytes2float(byte a, byte b, byte c, byte d) {
  float snelheid;

  union u_tag {
    byte b[4];
    float fval;
  } u;

  u.b[0] = a;
  u.b[1] = b;
  u.b[2] = c;
  u.b[3] = d;

  return snelheid = u.fval;
}


long lastPeriod = 0;
bool readEnable = false;
bool LaserOn = false;
//NFC side
uint8_t success;
uint8_t uid[] = { 0, 0, 0, 0, 0, 0, 0, 0 };  // Buffer to store the returned UID
uint8_t uiDisp[] = { 0, 0, 0, 0, 0, 0 };
uint8_t uidLength;                        // Length of the UID (4 or 7 bytes depending on ISO14443A card type)
bool ansCr = false;
bool ansSk = false;
bool answered = false;
bool answered2 = false;
char tagLife = ' ';
String mode = "";
float Cr = 0;
int Sk = 0;
bool timeout = true;
long timeout_tick = 0;


void loop() {

  //init state
  if (timeout) {
    digitalWrite(LASER, LOW);
    digitalWrite(6, LOW);
    digitalWrite(5, LOW);
    lc.clearDisplay(0);
    readEnable = true;
    answered = false;
    answered2 = false;
    timeout = false;
    Cr = -1;
    Sk = 0;
  }

  if (readEnable) {
    timeout_tick = millis();
    //read tag
    success = nfc.readPassiveTargetID(PN532_MIFARE_ISO14443A, uid, &sendSize);
    if (success) {
      // Display some basic information about the card
      Serial.println("Found an ISO14443A card");
      Serial.print("  UID Length: "); Serial.print(sendSize, DEC); Serial.println(" bytes");
      Serial.print("  UID Value: ");
      nfc.PrintHex(uid, sendSize);

      uid[0] = 'n';

      //send to gateway
      if (radio.sendWithRetry(GATEWAYID, uid, sendSize)) {
        Serial.print(" ok!");
      }
      else Serial.print(" nothing...");
      //display
      uiDisp[0] = uid[1];
      uiDisp[1] = uid[2];
      uiDisp[2] = uid[3];
      uiDisp[3] = uid[4];
      uiDisp[4] = uid[5];
      uiDisp[5] = uid[6];
      setDisplay(uiDisp);

      readEnable = false;
    }
  }

  if (radio.receiveDone()) {
    
    timeout_tick = millis();
    byte inByte[radio.DATALEN];
    
    Serial.print(radio.DATALEN);
    Serial.print(" - ");

    for (int i = 0; i < radio.DATALEN; i++) {
      inByte[i] = radio.DATA[i];
      Serial.print(inByte[i],DEC);
      Serial.print(" - ");
    }
    if (radio.ACKRequested()) radio.sendACK();
    Cr = bytes2float(inByte[0], inByte[1], inByte[2], inByte[3]);
    Serial.print("cr ");
    Serial.println(Cr);
    Sk = (int)inByte[4] - 48;
    printCr(Cr, Sk);

  }



  if (Cr >= 0) {
    
    digitalWrite(GREEN, HIGH);
    digitalWrite(LASER, HIGH);
    Serial.println(trigTime);
    if (trigTime > 110) {
      timeout_tick = millis();
      if (radio.sendWithRetry(GATEWAYID, "t", 1)) {
        Serial.print(" ok!");
        trigTime -= 110;
      }
    }

  }
  else {
    digitalWrite(LASER, LOW);
    digitalWrite(GREEN, LOW);
  }

  //se non succede nulla per più di 5 minuti riparti da capo?
  if ((millis() - timeout_tick) > 300000) {
    timeout = true;
    //reset all??
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

void printCr(float num, int sk) {
  uint8_t ones, tens, hundreds, thousands;
  int number = num * 10;

  thousands = number / 1000;
  number = number - thousands * 1000;

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
  if (num > 0) {
    lc.setDigit(0, 0, ones, false);
    lc.setDigit(0, 1, tens, true);
    if (num >= 10) {
      lc.setDigit(0, 2, hundreds, false);
      if (num >= 100) {
        lc.setDigit(0, 3, thousands, false);
      }
    }
  }
  else {
    lc.setDigit(0, 0, 0, false);
    lc.setDigit(0, 1, 0, true);
  }




}

