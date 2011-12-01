/*
 * Innovations ID-20 Pin-outs
 * http://www.sparkfun.com/products/8628
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
 *  9 D0  - RX1 Pin D19 on Arduino
 * 10 BZ  - 1Kohm resistor -> LED -> GND
 * 11 5V  - +5V
 *
 */

/*
 * DS18B20 One Wire Digital Temperature Sensor
 * http://www.sparkfun.com/products/245
 * http://datasheets.maxim-ic.com/en/ds/DS18B20.pdf
 *
 * With flat side facing you pins are read 1, 2, 3
 *
 *  1 GND    - GND
 *  2 RX Pin - Pins D10, D11 on Arduino
 *  3 VCC    - +5V
 *
 * Also connect a 4.7kOhm resistor between pin 2 and VCC
 *
 */

/*
 * Solid State Relay Kit
 * http://www.sparkfun.com/products/10684
 *
 * Pins are labelled:
 *
 * GND  - GND
 * CTRL - Pins D6, D7 on Arduino
 * 5V   - +5V
 *
 * The Absolute Maximum Load: 125VAC @ 8A
 *
 * Connect hot wire through load pins.  The relay does
 * not provide power, you must supply your own AC power.
 *
 */

/*
 * Serial Enabled 20x4 LCD - Black on Green 5V
 * http://www.sparkfun.com/products/9568
 *
 * RX  - Pin D2 on Arduino
 * GND - GND
 * VDD - +5V
 *
 */

/*
 * Flow sensors
 * SF800
 * http://www.swissflow.com/sf800.html
 *
 * RS = 232 Ohm
 * RL = ~2.2 KOhm
 *
 * Red   - RS -> +5V
 * Green - Pin D5 on Arduion, connect RL between this line and Red
 * Black - GND
 *
 */

/*
 * D-Sub Pinouts
 * 1 - T1   D10
 * 2 - F1   D20
 * 3 - T2   D11
 * 4 - F2   D21
 * 5 - 
 * 6 - LCD  D2
 * 7 - RFID D19
 * 8 -
 * 9 -
 *
 */

//--- Includes
#include <OneWire.h>
#include "SoftwareSerial.h"
#include "SparkFunSerLCD.h"
#include <Time.h>

//--- Analog Pin Allocations
// None

//--- Digital Pin Allocations
#define TP_PIN_LCD            2
#define TP_PIN_RELAY          7
#define TP_PIN_ONEWIRE_TEMP_1 10 // DS18B20 Transistor
#define TP_PIN_ONEWIRE_TEMP_2 11 // DS18B20 Transistor
#define TP_PIN_LED            12
#define TP_PIN_RFID           19 // Serial 1 from ID-20 reader
#define TP_PIN_FLOW_METER_1   20 // Interrupt 3
#define TP_PIN_FLOW_METER_2   21 // Interrupt 2

//--- Interrupt Numbers
#define TP_INTERRUPT_FLOW_METER_1 3 // Pin D20
#define TP_INTERRUPT_FLOW_METER_2 2 // Pin D21

//--- Tapkick Constants
#define TAP_DELAY 15
#define LCD_ROWS 4
#define LCD_COLS 20
#define FLOW_CONST 6100

//--- Instantiate Class Objects
OneWire ds1(TP_PIN_ONEWIRE_TEMP_1);
OneWire ds2(TP_PIN_ONEWIRE_TEMP_2);
SparkFunSerLCD lcd(TP_PIN_LCD, LCD_ROWS, LCD_COLS); // desired pin, rows, cols

//--- Globals
bool tapState = false;
time_t startTap = now();
byte lastcode[6];
volatile int flow1;
volatile int flow2;
float temperature1 = 0.0;
float temperature2 = 0.0;

//--- Tap Functions
void openTaps() {
  tapState = true;
  startTap = now();
  digitalWrite(TP_PIN_LED, HIGH);
  digitalWrite(TP_PIN_RELAY, HIGH);
}

void closeTaps() {
  tapState = false;
  startTap = now();
  digitalWrite(TP_PIN_LED, LOW);
  digitalWrite(TP_PIN_RELAY, LOW);
}

//--- Flow Functions
void resetFlow() {
  flow1 = 0;
  flow2 = 0;
}

void countFlow1() {
  flow1++;
}

void countFlow2() {
  flow2++;
}

//--- Temperature Functions
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
    Serial1.println("CRC is not valid!");
    return -1000;
  }

  if ( addr[0] != 0x10 && addr[0] != 0x28) {
    Serial1.print("Device is not recognized");
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

void setTemps() {
  //--- Get the temperature in Celcius
  temperature1 = getTemp(ds1);
  temperature2 = getTemp(ds2);
}

void printTemps() {
  //--- Print the temps to the lcd
  lcd.at(1,1,"Temp1:");
  lcd.at(1,7,int(temperature1));
  lcd.at(1,9,"C");
  lcd.at(1,11,"Temp2:");
  lcd.at(1,17,int(temperature2));
  lcd.at(1,19,"C");
}

//--- RFID Functions
void getRFID() {
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

  byte val = 0;
  byte code[6];
  byte checksum = 0;
  byte bytesread = 0;
  byte tempbyte = 0;

  if(Serial1.available() > 0) {
    if((val = Serial1.read()) == 2) {                  // check for header
      bytesread = 0; 
      while (bytesread < 12) {                        // read 10 digit code + 2 digit checksum
        if( Serial1.available() > 0) {
          val = Serial1.read();
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

      // Output to Serial1:

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

//--- Main Functions
void setup() {
  //--- Set up serial ports
  Serial.begin(9600);    // connect to the serial port (usb)
  Serial1.begin(9600);   // connect to the rfid

  //--- Set up pins
  pinMode(TP_PIN_LED, OUTPUT);
  pinMode(TP_PIN_RELAY, OUTPUT);
  pinMode(TP_PIN_FLOW_METER_1, INPUT);
  pinMode(TP_PIN_FLOW_METER_2, INPUT);

  //--- Attach interrupts
  // Need to set these HIGH so they won't just tick away
  digitalWrite(TP_PIN_FLOW_METER_1, HIGH);
  digitalWrite(TP_PIN_FLOW_METER_2, HIGH);
  attachInterrupt(TP_INTERRUPT_FLOW_METER_1, countFlow1, RISING);
  attachInterrupt(TP_INTERRUPT_FLOW_METER_2, countFlow2, RISING);

  //--- Setup Methods
  closeTaps();
  setTemps();
  printTemps();
  lcd.setup();
  lcd.at(3,2,"Welcome to Tapkick");
}

void loop () {
  
  getRFID();
  
  //--- Turn off Taps and print access
  if(tapState and (now() - startTap >= TAP_DELAY)) {
    cli(); // Clear Local Interrupts

    //--- Close the taps
    closeTaps();

    //--- Set the temps
    setTemps();

    //--- Print out the data for the access period
    for (int i=0; i<5; i++) {
      Serial.print(lastcode[i], HEX);
    }
    Serial.print(":");
    Serial.print(float(flow1));//float(FLOW_CONST));
    Serial.print("/");
    Serial.print(float(flow2));//float(FLOW_CONST));
    Serial.print("/");
    Serial.print(temperature1);
    Serial.print("/");
    Serial.print(temperature2);
    Serial.println();

    //--- Reset the flow now that you've printed it
    //resetFlow();

    //--- Print more info if we want
    lcd.empty();
    printTemps();
    lcd.at(3,2,"Rackers Love Beer");

    sei(); // Set Enable Interrupts
  }

}
