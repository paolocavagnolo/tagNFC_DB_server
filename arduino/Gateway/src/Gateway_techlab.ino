#include <RFM69.h>    //get it here: https://www.github.com/lowpowerlab/rfm69
#include <RFM69_ATC.h>//get it here: https://www.github.com/lowpowerlab/rfm69
#include <SPI.h>      //comes with Arduino IDE (www.arduino.cc)
#include <SPIFlash.h> //get it here: https://www.github.com/lowpowerlab/spiflash

//*********************************************************************************************
//************ IMPORTANT SETTINGS *************************************************************
//*********************************************************************************************
#define GATEWAYID     1
#define NETWORKID     100  //the same on all nodes that talk to each other
//Match frequency to the hardware version of the radio on your Moteino (uncomment one):
#define FREQUENCY     RF69_433MHZ
#define ENCRYPTKEY    "sampleEncryptKey" //exactly the same 16 characters/bytes on all nodes!
#define IS_RFM69HW    //uncomment only for RFM69HW! Leave out if you have RFM69W!
#define ENABLE_ATC    //comment out this line to disable AUTO TRANSMISSION CONTROL
#define SERIAL_BAUD   115200
//pinout
#define LED           9 // Moteinos have LEDs on D9
#define FLASH_SS      8 // and FLASH SS on D8
//*********************************************************************************************


//*********** RADIO *********//
#ifdef ENABLE_ATC
RFM69_ATC radio;
#else
RFM69 radio;
#endif


uint32_t packetCount = 0;

void setup() {
  Serial.begin(SERIAL_BAUD);
  delay(10);
  radio.initialize(FREQUENCY,GATEWAYID,NETWORKID);
#ifdef IS_RFM69HW
  radio.setHighPower(); //only for RFM69HW!
#endif
  radio.encrypt(ENCRYPTKEY);

  char buff[50];
  sprintf(buff, "\nListening at %d Mhz...", FREQUENCY==RF69_433MHZ ? 433 : FREQUENCY==RF69_868MHZ ? 868 : 915);
  Serial.println(buff);

#ifdef ENABLE_ATC
  Serial.println("RFM69_ATC Enabled (Auto Transmission Control)");
#endif
}

int idNode;
char payload[7];

void loop() {
  if (radio.receiveDone())
  {
    Serial.print('<');
    Serial.print(',');
    Serial.print(packetCount++);
    Serial.print(',');
    Serial.print(radio.SENDERID,DEC);
    Serial.print(',');
    Serial.print(1);
    Serial.print(',');
    Serial.print(radio.RSSI);
    for (byte i = 0; i < radio.DATALEN; i++) {
      Serial.print(',');
      Serial.print(radio.DATA[i],HEX);
    }
    Serial.print(',');
    Serial.println('>');
    //Check
    if (radio.ACKRequested()) radio.sendACK();
  }

  if (Serial.available() > 0)
  {
     payload = {0,1,2,3,4,5,6};
     radio.sendWithRetry(2, payload, 7);
  }
}
