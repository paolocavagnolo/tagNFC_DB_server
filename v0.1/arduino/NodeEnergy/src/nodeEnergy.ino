#include <RFM69.h>         //get it here: https://www.github.com/lowpowerlab/rfm69
#include <SPI.h>
#include <avr/io.h>
#include <avr/interrupt.h>
#include <SPIFlash.h>      //get it here: https://www.github.com/lowpowerlab/spiflash
#include <avr/wdt.h>
#include <WirelessHEX69.h> //get it here: https://github.com/LowPowerLab/WirelessProgramming/tree/master/WirelessHEX69
#include <avr/io.h>
#include <avr/wdt.h>


#define Reset_AVR() wdt_enable(WDTO_30MS); while(1) {}

#define NODEID      4       // node ID used for this unit
#define NETWORKID   100
#define GATEWAYID   1

#define FREQUENCY   RF69_433MHZ

#define IS_RFM69HW  //uncomment only for RFM69HW! Leave out if you have RFM69W!
#define SERIAL_BAUD 115200
#define ACK_TIME    30  // # of ms to wait for an ack
#define ENCRYPTKEY "sampleEncryptKey" //(16 bytes of your choice - keep the same on all encrypted nodes)

#define LED           9 // Moteinos hsave LEDs on D9
#define FLASH_SS      8 // and FLASH SS on D8

uint32_t MEMSHIFT = 100000;

uint32_t MEMA1 = 48+MEMSHIFT;
uint32_t MEMA2 = 5048+MEMSHIFT;
uint32_t MEMB1 = 10048+MEMSHIFT;
uint32_t MEMB2 = 15048+MEMSHIFT;
uint32_t MEMC1 = 20048+MEMSHIFT;
uint32_t MEMC2 = 25048+MEMSHIFT;

#define COUNT_TICK 20

byte sendSize = 6;
boolean requestACK = false;

float totenA = 0;
byte totenA_b[4];

float totenB = 0;
byte totenB_b[4];

float totenC = 0;
byte totenC_b[4];

RFM69 radio;
char input = 0;
long lastPeriod = -1;

/////////////////////////////////////////////////////////////////////////////
// flash(SPI_CS, MANUFACTURER_ID)
// SPI_CS          - CS pin attached to SPI flash chip (8 in case of Moteino)
// MANUFACTURER_ID - OPTIONAL, 0x1F44 for adesto(ex atmel) 4mbit flash
//                             0xEF30 for windbond 4mbit flash
//                             0xEF40 for windbond 16/64mbit flash
/////////////////////////////////////////////////////////////////////////////
SPIFlash flash(FLASH_SS, 0xEF30); //EF30 for windbond 4mbit flash

float tA, tB, tC;
bool fA, fB, fC;

void pciSetup(byte pin)
{
    *digitalPinToPCMSK(pin) |= bit (digitalPinToPCMSKbit(pin));  // enable pin
    PCIFR  |= bit (digitalPinToPCICRbit(pin)); // clear any outstanding interrupt
    PCICR  |= bit (digitalPinToPCICRbit(pin)); // enable interrupt for the group
}

ISR (PCINT1_vect) // handle pin change interrupt for A0 to A5 here
{
    tA++;
}

ISR (PCINT0_vect) // handle pin change interrupt for D8 to D13 here
{
    tC++;
}

ISR (PCINT2_vect) // handle pin change interrupt for D0 to D7 here
{
   tB++;
}

void setup(){
  pinMode(LED, OUTPUT);
  radio.initialize(FREQUENCY,NODEID,NETWORKID);
  radio.encrypt(ENCRYPTKEY); //OPTIONAL
  #ifdef IS_RFM69HW
    radio.setHighPower(); //only for RFM69HW!
  #endif
  
  flash.initialize();

  byte max_b[4], max2_b[4];
  float max, max2;

  //read totalEnergy A
  flash.readBytes(MEMA1,max_b,4);
  max = bytes2Float(&max_b[0]);
  flash.readBytes(MEMA2,max2_b,4);
  max2 = bytes2Float(&max2_b[0]);
  if (max2 >= max) {
    totenA = max2;
  }
  else {
    totenA = max;
  }

  //read totalEnergy B
  flash.readBytes(MEMB1,max_b,4);
  max = bytes2Float(&max_b[0]);
  flash.readBytes(MEMB2,max2_b,4);
  max2 = bytes2Float(&max2_b[0]);
  if (max2 >= max) {
    totenB = max2;
  }
  else {
    totenB = max;
  }

  //read totalEnergy C
  flash.readBytes(MEMC1,max_b,4);
  max = bytes2Float(&max_b[0]);
  flash.readBytes(MEMC2,max2_b,4);
  max2 = bytes2Float(&max2_b[0]);
  if (max2 >= max) {
    totenC = max2;
  }
  else {
    totenC = max;
  }

  //enable interrupt for pin ...
  pciSetup(4);
  pciSetup(9);
  pciSetup(A2);
}



char message[5];
long timeoutMAX = 60000000;


void loop(){

  if (millis() > timeoutMAX) {
    Reset_AVR();
  }

  if (radio.receiveDone()) {

    byte inByte[radio.DATALEN];

    for (int i = 0; i < radio.DATALEN; i++) {
      inByte[i] = radio.DATA[i];
    }

    if (radio.ACKRequested()) radio.sendACK();
  
    byte cc[4] = {inByte[1],inByte[2],inByte[3],inByte[4]};
    float count = bytes2Float(&cc[0]);
    switch ((char)inByte[0]) {
      case 'a':
        totenA = count;
        tA = 0;
        break;

      case 'b':
        totenB = count;
        tB = 0;
        break;

      case 'c':
        totenC = count;
        tC = 0;
        break;

      default:
        break;
    }

  }

  if (tA>=COUNT_TICK) {
    tA = tA - COUNT_TICK;
    totenA = totenA + 0.01;
    //totenA = 48.67;
    float2Bytes(totenA,&totenA_b[0]);
    flash.blockErase4K(MEMA1);
    while(flash.busy());
    flash.writeBytes(MEMA1,totenA_b,4);
    flash.blockErase4K(MEMA2);
    while(flash.busy());
    flash.writeBytes(MEMA2,totenA_b,4);

    message[0] = 'e';
    message[1] = 'a';
    message[2] = totenA_b[0];
    message[3] = totenA_b[1];
    message[4] = totenA_b[2];
    message[5] = totenA_b[3];

    //send to gateway
    radio.sendWithRetry(GATEWAYID, message, sendSize);
  }

  if (tB>=COUNT_TICK) {
    tB = tB - COUNT_TICK;
    totenB = totenB + 0.01;
    //totenB = 42.00;
    float2Bytes(totenB,&totenB_b[0]);
    flash.blockErase4K(MEMB1);
    while(flash.busy());
    flash.writeBytes(MEMB1,totenB_b,4);
    flash.blockErase4K(MEMB2);
    while(flash.busy());
    flash.writeBytes(MEMB2,totenB_b,4);

    message[0] = 'e';
    message[1] = 'b';
    message[2] = totenB_b[0];
    message[3] = totenB_b[1];
    message[4] = totenB_b[2];
    message[5] = totenB_b[3];
    
    radio.sendWithRetry(GATEWAYID, message, sendSize);

  }

  if (tC>=COUNT_TICK) {
    tC = tC - COUNT_TICK;
    totenC = totenC + 0.01;
    //totenC = 24.63;
    float2Bytes(totenC,&totenC_b[0]);
    flash.blockErase4K(MEMC1);
    while(flash.busy());
    flash.writeBytes(MEMC1,totenC_b,4);
    flash.blockErase4K(MEMC2);
    while(flash.busy());
    flash.writeBytes(MEMC2,totenC_b,4);

    message[0] = 'e';
    message[1] = 'c';
    message[2] = totenC_b[0];
    message[3] = totenC_b[1];
    message[4] = totenC_b[2];
    message[5] = totenC_b[3];

    radio.sendWithRetry(GATEWAYID, message, sendSize);
  }
// end loop 

}

void float2Bytes(float val,byte* bytes_array){
  // Create union of shared memory space
  union {
    float float_variable;
    byte temp_array[4];
  } u;
  // Overite bytes of union with float variable
  u.float_variable = val;
  // Assign bytes to input array
  memcpy(bytes_array, u.temp_array, 4);
}

float bytes2Float(byte* bytes_array) {
  float val;

  union {
    float fval;
    byte b[4];
  } u;

  u.b[0] = bytes_array[0];
  u.b[1] = bytes_array[1];
  u.b[2] = bytes_array[2];
  u.b[3] = bytes_array[3];

  val = u.fval;
  return val;
}

