/* 
        NOTE: you must: #include "SoftwareSerial.h"
        BEFORE including the class header file
        
                                allen joslin
                                payson productions
                                allen@joslin.net
*/

#include "SoftwareSerial.h"
#include "SparkFunSerLCD.h"

/* ======================================================== */

#define PINOUT      0
#define POSBASE     1
#define BOUNCE      2
#define NUMROWS     3
#define NUMCOLS     4
#define LASTROW     5
#define LASTCOL     6
#define LASTBRIGHT  7 

//--------------------------
SparkFunSerLCD::SparkFunSerLCD ( int pin, int numRows, int numCols, int posBase ) 
        : SoftwareSerial(pin,pin) {
        _bv[PINOUT]=pin;
        _bv[POSBASE]=posBase;
        _bv[BOUNCE]=4;
        _bv[NUMROWS]=numRows;
        _bv[NUMCOLS]=numCols;
        _bv[LASTROW]=1;
        _bv[LASTCOL]=1;
        _bv[LASTBRIGHT]=100;
        _ro[0]=0;
        _ro[1]=64;
        _ro[2]=numCols;
        _ro[3]=_ro[1]+numCols;
}

//--------------------------
void SparkFunSerLCD::setup( int startPcnt, boolean startEmpty ) {
        pinMode(_bv[PINOUT], OUTPUT);
        delay(_bv[BOUNCE]);
        begin(9600);
        delay(_bv[BOUNCE]);
        if (startEmpty) {
                empty(); 
        }
        bright(startPcnt);
        cursorOff();
}

//--------------------------
void SparkFunSerLCD::on () { 
        print(0xfe,BYTE); delay(_bv[BOUNCE]); 
        print(0x0c,BYTE); delay(_bv[BOUNCE]); 
}

//--------------------------
void SparkFunSerLCD::off () { 
        print(0xfe,BYTE); delay(_bv[BOUNCE]); 
        print(0x08,BYTE); delay(_bv[BOUNCE]); 
}

//--------------------------
void SparkFunSerLCD::scrollLeft () { 
        print(0xfe,BYTE); delay(_bv[BOUNCE]); 
        print(0x18,BYTE); delay(_bv[BOUNCE]); 
}

//--------------------------
void SparkFunSerLCD::scrollRight () { 
        print(0xfe,BYTE); delay(_bv[BOUNCE]); 
        print(0x1c,BYTE); delay(_bv[BOUNCE]); 
}

//--------------------------
void SparkFunSerLCD::empty () { 
        print(0xfe,BYTE); delay(_bv[BOUNCE]); 
        print(0x01,BYTE); delay(_bv[BOUNCE]*10); 
}

//--------------------------
void SparkFunSerLCD::cursorUnderline () { 
        print(0xfe,BYTE); delay(_bv[BOUNCE]); 
        print(0x0e,BYTE); delay(_bv[BOUNCE]); 
}

//--------------------------
void SparkFunSerLCD::cursorBlock () { 
        print(0xfe,BYTE); delay(_bv[BOUNCE]); 
        print(0x0d,BYTE); delay(_bv[BOUNCE]); 
}

//--------------------------
void SparkFunSerLCD::cursorOff () { 
        print(0xfe,BYTE); delay(_bv[BOUNCE]); 
        print(0x0c,BYTE); delay(_bv[BOUNCE]); 
}

//--------------------------
void SparkFunSerLCD::bright ( int pcnt ) {
        if (_bv[LASTBRIGHT] == pcnt) { return; }
        pcnt = (pcnt<0)?0:pcnt;
        pcnt = (pcnt>100)?100:pcnt;
        print(0x7c,BYTE); delay(_bv[BOUNCE]); 
        print(128+(pcnt*30/100),BYTE); delay(_bv[BOUNCE]); 
        _bv[LASTBRIGHT] = pcnt;
}

//--------------------------
void SparkFunSerLCD::pos ( int row, int col ) 
{ 
        print(0xfe,BYTE); delay(_bv[BOUNCE]); 
        print(0x80 + _ro[(row - _bv[POSBASE])] + (col - _bv[POSBASE]),BYTE); delay(_bv[BOUNCE]); 
}

// shortcuts

void SparkFunSerLCD::at ( int row, int col, char v )            { pos(row,col); print(v); }
void SparkFunSerLCD::at ( int row, int col, const char v[] )    { pos(row,col); print(v); }
void SparkFunSerLCD::at ( int row, int col, uint8_t v )         { pos(row,col); print(v); }
void SparkFunSerLCD::at ( int row, int col, int v )             { pos(row,col); print(v); }
void SparkFunSerLCD::at ( int row, int col, unsigned int v )    { pos(row,col); print(v); }
void SparkFunSerLCD::at ( int row, int col, long v )            { pos(row,col); print(v); }
void SparkFunSerLCD::at ( int row, int col, unsigned long v )   { pos(row,col); print(v); }
void SparkFunSerLCD::at ( int row, int col, long v, int t )     { pos(row,col); print(v,t); }


/* ======================================================== */
