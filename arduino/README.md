# Installation and Use

To use the tapkick arduino you must follow these steps:

1. Upload the arduino code to your arduino Mega

2. Install the following libraries to your system:

    $ pip install pyserial

3. Run the python code to read from the serial port

    $ ./tapkick.py

4. Watch the output

# Hardware Reference

## Innovations ID-20 Pin-outs

 http://www.sparkfun.com/products/8628
 http://www.sparkfun.com/datasheets/Sensors/ID-12-Datasheet.pdf

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


## DS18B20 One Wire Digital Temperature Sensor

 http://www.sparkfun.com/products/245
 http://datasheets.maxim-ic.com/en/ds/DS18B20.pdf

 With flat side facing you pins are read 1, 2, 3

*  1 GND    - GND
*  2 RX Pin - Pins D10, D11 on Arduino
*  3 VCC    - +5V

 Also connect a 4.7kOhm resistor between pin 2 and VCC


## Solid State Relay Kit

 http://www.sparkfun.com/products/10684

 Pins are labelled:

* GND  - GND
* CTRL - Pins D6, D7 on Arduino
* 5V   - +5V

 The Absolute Maximum Load: 125VAC @ 8A

 Connect hot wire through load pins.  The relay does
 not provide power, you must supply your own AC power.


## Serial Enabled 20x4 LCD - Black on Green 5V
 
 http://www.sparkfun.com/products/9568

* RX  - Pin D2 on Arduino
* GND - GND
* VDD - +5V


## Flow sensor SF800

 http://www.swissflow.com/sf800.html

* RS = 232 Ohm
* RL = ~2.2 KOhm

* Red   - RS -> +5V
* Green - Pin D5 on Arduion, connect RL between this line and Red
* Black - GND


## D-Sub Pinouts

* 1 - T1   D10
* 2 - F1   D20
* 3 - T2   D11
* 4 - F2   D21
* 5 - 
* 6 - LCD  D2
* 7 - RFID D19
* 8 -
* 9 -

