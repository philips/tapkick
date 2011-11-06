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

//--- Digital Pins
#define rfid         0
#define tap1solenoid 6
#define tap2solenoid 7


void setup() {
  Serial.begin(9600);                                 // connect to the serial port

  //--- Set up Solenoid Valves
  pinMode(tap1solenoid, OUTPUT);
  digitalWrite(tap1solenoid, LOW);
  pinMode(tap2solenoid, OUTPUT);
  digitalWrite(tap2solenoid, LOW);

}

void loop () {
  byte i = 0;
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
        Serial.print("5-byte code: ");
        for (i=0; i<5; i++) {
          if (code[i] < 16) Serial.print("0");
          Serial.print(code[i], HEX);
          Serial.print(" ");
        }
        Serial.println();

        Serial.print("Checksum: ");
        Serial.print(code[5], HEX);
        Serial.println(code[5] == checksum ? " -- passed." : " -- error.");
        Serial.println();
        
        //--- Turn on Taps
        digitalWrite(tap1solenoid, HIGH);
        digitalWrite(tap2solenoid, HIGH);
      }

      bytesread = 0;
      
      //--- Turn off Taps
      delay(1000);
      digitalWrite(tap1solenoid, LOW);
      digitalWrite(tap2solenoid, LOW);
    }
  }
}
