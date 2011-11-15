
// RFID reader ID-20 for Arduino 
//
// Based on code by BARRAGAN <http://people.interaction-ivrea.it/h.barragan> 
// and code from HC Gilje - http://hcgilje.wordpress.com/resources/rfid_id12_tagreader/
// Modified for Arudino by djmatic
// Modified for ID-12 and checksum by Martijn The - http://www.martijnthe.nl/
//
// Use the drawings from HC Gilje to wire up the ID-12.
// Remark: disconnect the rx serial wire to the ID-12 when uploading the sketch
// Source: http://www.arduino.cc/playground/Code/ID12

/*
 * Innovations ID-20 Pin-outs
 * http://www.sparkfun.com/datasheets/Sensors/ID-12-Datasheet.pdf
 * 
 *  1 GND - GND
 *  2 RST - +5V
 *  3 ANT - None
 *  4 ANT - None
 *  5 CP  - None
 *  6 NC  - None
 *  7 FS  - GND
 *  8 D1  - None
 *  9 D0  - RX Pin D0 on Arduino
 * 10 BZ  - 1Kohm resistor -> LED -> GND
 * 11 5V  - +5V
 * 
 */
 
//--- Includes
#include <OneWire.h>
#include <Time.h>

//--- Digital Pins
#define rfid         0
#define tap1solenoid 6
#define tap2solenoid 7
#define temp1        10 // DS18B20 Transistor
#define temp2        11 // DS18B20 Transistor

//--- Constants
#define TAP_DELAY 5

//--- Instantiate Class Objects
OneWire ds1(temp1);
OneWire ds2(temp2);

//--- Globals
time_t startTap = 0;
byte lastcode[6];
float flow1 = 0.0;
float flow2 = 0.0;

//--- Functions
void openTaps() {
  startTap = now();
  digitalWrite(tap1solenoid, HIGH);
  digitalWrite(tap2solenoid, HIGH);
}

void closeTaps() {
  startTap = 0;
  digitalWrite(tap1solenoid, LOW);
  digitalWrite(tap2solenoid, LOW);
}

void resetFlow() {
  flow1 = 0.0;
  flow2 = 0.0;
}

void addFlow() {
  flow1 += 1.0;
  flow2 += 1.0;
}

float getTemp(OneWire ds){
  // from http://bildr.org/2011/07/ds18b20-arduino/
  // returns the temperature from one DS18S20 in DEG Celsius

  byte data[12];
  byte addr[8];

  if ( !ds.search(addr)) {
  //no more sensors on chain, reset search
     ds.reset_search();
  return -1000;
  }

  if ( OneWire::crc8( addr, 7) != addr[7]) {
    Serial.println("CRC is not valid!");
    return -1000;
  }

  if ( addr[0] != 0x10 && addr[0] != 0x28) {
    Serial.print("Device is not recognized");
    return -1000;
  }

  ds.reset();
  ds.select(addr);
  ds.write(0x44,1); // start conversion, with parasite power on at the end

  byte present = ds.reset();
  ds.select(addr);
  ds.write(0xBE); // Read Scratchpad


  for (int i = 0; i < 9; i++) { // we need 9 bytes
    data[i] = ds.read();
  }

  ds.reset_search();

  byte MSB = data[1];
  byte LSB = data[0];

  float tempRead = ((MSB << 8) | LSB); //using two's compliment
  float TemperatureSum = tempRead / 16;

  return TemperatureSum;

}

void getRFID() {
  byte val = 0;
  byte code[6];
  byte checksum = 0;
  byte bytesread = 0;
  byte tempbyte = 0;

  if(Serial.available() > 0) {
    if((val = Serial.read()) == 2) {                  // check for header 
      bytesread = 0; 
      while (bytesread < 12) {                        // read 10 digit code + 2 digit checksum
        if( Serial.available() > 0) { 
          val = Serial.read();
          if((val == 0x0D)||(val == 0x0A)||(val == 0x03)||(val == 0x02)) { // if header or stop bytes before the 10 digit reading 
            break;                                    // stop reading
          }

          // Do Ascii/Hex conversion:
          if ((val >= '0') && (val <= '9')) {
            val = val - '0';
          } else if ((val >= 'A') && (val <= 'F')) {
            val = 10 + val - 'A';
          }

          // Every two hex-digits, add byte to code:
          if (bytesread & 1 == 1) {
            // make some space for this hex-digit by
            // shifting the previous hex-digit with 4 bits to the left:
            code[bytesread >> 1] = (val | (tempbyte << 4));

            if (bytesread >> 1 != 5) {                // If we're at the checksum byte,
              checksum ^= code[bytesread >> 1];       // Calculate the checksum... (XOR)
            };
          } else {
            tempbyte = val;                           // Store the first hex digit first...
          };

          bytesread++;                                // ready to read next digit
        } 
      } 

      // Output to Serial:

      if (bytesread == 12) {                          // if 12 digit read is complete
        for (int i=0; i<5; i++) {
          lastcode[i] = code[i];
        }
        
        //--- Turn on Taps
        openTaps();
      }

      bytesread = 0;
    }
  }
}

void setup() {
  Serial.begin(9600);                                 // connect to the serial port

  //--- Set up Solenoid Valves
  pinMode(tap1solenoid, OUTPUT);
  pinMode(tap2solenoid, OUTPUT);
  closeTaps();
}

void loop () {

  getRFID();

  //--- Turn off Taps
  if(startTap > 0 and (now() - startTap >= TAP_DELAY)) {
    //--- Close the taps
    closeTaps();

    //--- Get the temperature in Celcius
    float temperature1 = getTemp(ds1);
    float temperature2 = getTemp(ds2);

    //--- Print out the data for the access period
    for (int i=0; i<5; i++) {
      Serial.print(lastcode[i], HEX);
      Serial.print(" ");
    }
    Serial.print(": ");
    Serial.print(flow1);
    Serial.print("/");
    Serial.print(flow2);
    Serial.print("/");
    Serial.print(temperature1);
    Serial.print("/");
    Serial.print(temperature2);
    Serial.println();
    
    //--- Reset the flow now that you've printed it
    resetFlow();
  } else {
    addFlow();
  }

}
