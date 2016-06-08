#include <RFM69.h>    //get it here: https://www.github.com/lowpowerlab/rfm69
#include <RFM69_ATC.h>//get it here: https://www.github.com/lowpowerlab/rfm69
#include <SPI.h>      //comes with Arduino IDE (www.arduino.cc)
#include <SPIFlash.h> //get it here: https://www.github.com/lowpowerlab/spiflash
#include <WirelessHEX69.h> //get it here: https://github.com/LowPowerLab/WirelessProgramming/tree/master/WirelessHEX69


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
#define ACK_TIME      50  // # of ms to wait for an ack
#define TIMEOUT       3000
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
char c = 0;
byte targetID=0;
char input[64]; //serial input buffer

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
     String input_s = Serial.readString();
     byte inputLen = input_s.length();
     input_s.toCharArray(input, inputLen);

     if (inputLen==4 && input[0]=='F' && input[1]=='L' && input[2]=='X' && input[3]=='?') {
       if (targetID==0)
         Serial.println("TO?");
       else
         CheckForSerialHEX((byte*)input, inputLen, radio, targetID, TIMEOUT, ACK_TIME, false);
     }
     else if (inputLen>3 && inputLen<=6 && input[0]=='T' && input[1]=='O' && input[2]==':')
     {
       byte newTarget=0;
       for (byte i = 3; i<inputLen; i++) //up to 3 characters for target ID
         if (input[i] >=48 && input[i]<=57)
           newTarget = newTarget*10+input[i]-48;
         else
         {
           newTarget=0;
           break;
         }
       if (newTarget>0)
       {
         targetID = newTarget;
         Serial.print("TO:");
         Serial.print(newTarget);
         Serial.println(":OK");
       }
       else
       {
         Serial.print(input);
         Serial.print(":INV");
       }
     }
     else if (inputLen>0) { //just echo back
       if (input_s[0] == 'i') {
         input_s.remove(0,1);
         idNode = input_s.toInt();
       }
       else if (input_s[0] == 'j') {
         input_s.remove(0,1);
         uint8_t payload[input_s.length()];
         for (uint8_t i=0; i<input_s.length(); i++) {
           payload[i] = input_s[i];
         }
         radio.sendWithRetry(idNode, payload, input_s.length());
       }
     }

  }
}
