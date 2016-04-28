#include <SPI.h>
#include <Wire.h>
#include <RFM69.h>        //get it here: https://www.github.com/lowpowerlab/rfm69
#include <RFM69_ATC.h>    //get it here: https://www.github.com/lowpowerlab/rfm69
#include <SPIFlash.h>     //get it here: https://www.github.com/lowpowerlab/spiflash

//*********************************************************************************************
//************ IMPORTANT SETTINGS - YOU MUST CHANGE/CONFIGURE TO FIT YOUR HARDWARE *************
//*********************************************************************************************
//RFM side
#define NODEID        4    //must be unique for each node on same network (range up to 254, 255 is used for broadcast)
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

//Flash side
SPIFlash flash(FLASH_SS, 0xEF30); //EF30 for 4mbit  Windbond chip (W25X40CL)

#ifdef ENABLE_ATC
RFM69_ATC radio;
#else
RFM69 radio;
#endif

#define MEMA1 48
#define MEMA2 5048
#define MEMB1 10048
#define MEMB2 15048
#define MEMC1 20048
#define MEMC2 25048

float totenA = 0;
byte totenA_b[4];

float totenB = 0;
byte totenB_b[4];

float totenC = 0;
byte totenC_b[4];

void setup() {
  Serial.begin(SERIAL_BAUD);

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

}



void loop() {

  if (digitalRead(6)>0) {
    totenA = totenA + 0.001;
    //totenA = 21.73;
    float2Bytes(totenA,&totenA_b[0]);
    flash.blockErase4K(MEMA1);
    while(flash.busy());
    flash.writeBytes(MEMA1,totenA_b,4);
    flash.blockErase4K(MEMA2);
    while(flash.busy());
    flash.writeBytes(MEMA2,totenA_b,4);

    Serial.print("A: ");
    Serial.println(totenA);
    delay(20);
  }

  if (digitalRead(5)>0) {
    totenB = totenB + 0.001;
    //totenB = 29.11;
    float2Bytes(totenB,&totenB_b[0]);
    flash.blockErase4K(MEMB1);
    while(flash.busy());
    flash.writeBytes(MEMB1,totenB_b,4);
    flash.blockErase4K(MEMB2);
    while(flash.busy());
    flash.writeBytes(MEMB2,totenB_b,4);

    Serial.print("B: ");
    Serial.println(totenB);
    delay(20);
  }

  if (digitalRead(4)>0) {
    totenC = totenC + 0.001;
    //totenC = 14.78;
    float2Bytes(totenC,&totenC_b[0]);
    flash.blockErase4K(MEMC1);
    while(flash.busy());
    flash.writeBytes(MEMC1,totenC_b,4);
    flash.blockErase4K(MEMC2);
    while(flash.busy());
    flash.writeBytes(MEMC2,totenC_b,4);

    Serial.print("C: ");
    Serial.println(totenC);
    delay(20);
  }

  int currPeriod = millis()/TRANSMITPERIOD;
  if (currPeriod < lastPeriod) {
     lastPeriod=currPeriod;

   }
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
