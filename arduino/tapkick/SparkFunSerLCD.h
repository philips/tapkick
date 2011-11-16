/* 
        NOTE: you must: #include <SoftwareSerial.h>
        BEFORE including the class header file
        
                                allen joslin
                                payson productions
                                allen@joslin.net
*/

#ifndef SparkFunSerLCD_h
#define SparkFunSerLCD_h

#include "WProgram.h"

/******************************************************************************************************/
/* SparkFunSerLCD -- manages the SparkFun SerLCD, based on SoftwareSerial to aid pinning and printing */
/*                                                                                                    */
/*     some cmds are cached so repeated calls will not actually be sent which can cause               */
/*     flickering of the display, printed values are not cached and are always sent                   */
/*                                                                                                    */
/*     autoOn: turn off the display and turn it back on with the next command                         */
/*                                                                                                    */
/*     posBase: cursor positioning via 0x0 or 1x1                                                     */
/*                                                                                                    */
/*     on/off: display of characters, not backlight                                                   */
/*                                                                                                    */
/*     bright: backlight control, by percentage                                                       */
/*                                                                                                    */
/*     scrolling: scrolling is slow because of the amount of time the LCD takes to redraw.            */
/*     scrolling is persistant and moves the x-origin a single column at a time                       */
/*                                                                                                    */
/******************************************************************************************************/

class SparkFunSerLCD : public SoftwareSerial {
private:
        int _bv[9];
        int _ro[5];

public:
   SparkFunSerLCD ( int pin, int numRows, int numCols, int posBase=1 );
   void setup ( int brightPcnt=100, boolean startEmpty=true ); 

   void on ();
   void off ();

   void empty ();

   void scrollLeft ();
   void scrollRight ();

   void bright ( int pcnt );
   void pos ( int row, int col );

   void cursorUnderline();
   void cursorBlock();
   void cursorOff ();

        // shortcuts for printing at particular positions
   void at ( int row, int col, char );
   void at ( int row, int col, const char[] );
   void at ( int row, int col, uint8_t );
   void at ( int row, int col, int );
   void at ( int row, int col, unsigned int );
   void at ( int row, int col, long );
   void at ( int row, int col, unsigned long );
   void at ( int row, int col, long, int );

};


#endif
