#include <RFM69.h>    //get it here: https://www.github.com/lowpowerlab/rfm69
#include <RFM69_ATC.h>//get it here: https://www.github.com/lowpowerlab/rfm69
#include <SPI.h>      //comes with Arduino IDE (www.arduino.cc)
#include <SPIFlash.h> //get it here: https://www.github.com/lowpowerlab/spiflash

//*********************************************************************************************
//************ IMPORTANT SETTINGS - YOU MUST CHANGE/CONFIGURE TO FIT YOUR HARDWARE *************
//*********************************************************************************************
#define GATEWAYID     1
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

#define LED           9 // Moteinos have LEDs on D9
#define FLASH_SS      8 // and FLASH SS on D8

#ifdef ENABLE_ATC
RFM69_ATC radio;
#else
RFM69 radio;
#endif

SPIFlash flash(FLASH_SS, 0xEF30); //EF30 for 4mbit  Windbond chip (W25X40CL)
bool promiscuousMode = false; //set to 'true' to sniff all packets on the same network

uint8_t CheckTresh = 0;

void setup() {
  Serial.begin(SERIAL_BAUD);
  delay(10);
  radio.initialize(FREQUENCY, GATEWAYID, NETWORKID);
#ifdef IS_RFM69HW
  radio.setHighPower(); //only for RFM69HW!
#endif
  radio.encrypt(ENCRYPTKEY);
  radio.promiscuous(promiscuousMode);
  //radio.setFrequency(919000000); //set frequency to some custom frequency

  flash.initialize();

}

byte ackCount = 0;
uint32_t packetCount = 0;
uint8_t dataRecevied[7];
int Cr = 0; //credits
int Ab = 0; //abilitation code
byte incomingByte[5];
byte sendSize = 1;

byte serial2radio[12];
uint8_t idNode = 0;
byte TypeFromNode;
byte TypeFromGateway;
byte MessageFromNode[8];
byte MessageToNode[8];
int8_t RSSInode;

void loop() {
  //Read from node and sendit to serial
  switch (recieveFromNodes()) {
    case 'z':
      Serial.println("m: Error in check treshold of incremental number **POSSIBLE ATTACK!**");
      break;

    case 'a':
      //Send to Serial
      Serial.print('<');
      Serial.print(idNode);
      Serial.print(CheckTresh);
      Serial.print((char)TypeFromNode);
      PrintHex8(MessageFromNode,8);
      Serial.print(RSSInode);
      Serial.println('>');
      break;
  }
  //Read from serial and sendit to node
  if (Serial.available() > 0)
  {
    for (int i=0;i<12;i++) {
      serial2radio[i] = (char)Serial.read();
    }
    for (int i=0;i<8;i++) MessageToNode[i] = serial2radio[3+i];
    sendToNode(serial2radio[1], serial2radio[2], MessageToNode);
  }

}

void Blink(byte PIN, int DELAY_MS)
{
  pinMode(PIN, OUTPUT);
  digitalWrite(PIN, HIGH);
  delay(DELAY_MS);
  digitalWrite(PIN, LOW);
}

int sendToNode(uint8_t nodeid, char type, byte message[8]) {
  MessageToNode[0] = '<';       //SoC
  MessageToNode[1] = nodeid;    //Node ID
  CheckTresh++;
  if (CheckTresh > 254) {
    CheckTresh = 0;
  }
  MessageToNode[2] = (char)(CheckTresh);  //Security incremental
  MessageToNode[3] = type;
  for (int i=0; i<8; i++) MessageToNode[4+i] = message[i];
  MessageToNode[12] = '>';

  return radio.sendWithRetry(nodeid, MessageToNode, 13);

}

byte zeros[] = {'0','0','0','0','0','0','0','0'};

char recieveFromNodes(){
  if (radio.receiveDone()) {
    if (radio.ACKRequested()) radio.sendACK();
    idNode = radio.SENDERID;
    //Check incremental variable
    if (radio.DATA[2] == 'k'){
      sendToNode(idNode,'k',zeros);
    }
    else {
      if (radio.DATA[2] > CheckTresh) {
        CheckTresh + 1;
      }
      else {
        return 'z';
      }
    }

    TypeFromNode = radio.DATA[3];
    for (int i=0; i<8; i++) MessageFromNode[i] = radio.DATA[4+i];
    RSSInode = radio.RSSI;
    return 'a';
  }
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
    //tmp[i * 5] = 48; // add leading 0
    //tmp[i * 5 + 1] = 120; // add leading x
    tmp[i * 5 + 2] = first + 48;
    tmp[i * 5 + 3] = second + 48;
    //tmp[i * 5 + 4] = 32; // add trailing space
    if (first > 9) tmp[i * 5 + 2] += 7;
    if (second > 9) tmp[i * 5 + 3] += 7;
  }
  tmp[length * 5] = 0;
  Serial.print(tmp);
}
