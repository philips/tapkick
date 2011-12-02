/**                                                                                                            
 * Copyright 2011 Chris Gilmer <chris.gilmer@gmail.com>                      
 *                                                                                                             
 * This file is part of the Tapkick project.               
 * For more information on Tapkick, see https://github.com/philips/tapkick                      
 *                                                                                                             
 * Tapkick is free software: you can redistribute it and/or modify               
 * it under the terms of the GNU General Public License as published by         
 * the Free Software Foundation, either version 2 of the License, or            
 * (at your option) any later version.                                                                         
 *                                                                                                             
 * Tapkick is distributed in the hope that it will be useful,                    
 * but WITHOUT ANY WARRANTY; without even the implied warranty of               
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                
 * GNU General Public License for more details.                                                                
 *                                                                                                             
 * You should have received a copy of the GNU General Public License            
 * along with Tapkick.  If not, see <http://www.gnu.org/licenses/>.              
 */                                                                                                            

//--- Analog Pin Allocations
// None

//--- Digital Pin Allocations
#define TP_PIN_LCD            2
#define TP_PIN_RELAY          7
#define TP_PIN_ONEWIRE_TEMP_1 10 // DS18B20 Transistor
#define TP_PIN_ONEWIRE_TEMP_2 11 // DS18B20 Transistor
#define TP_PIN_LED            12
#define TP_PIN_RFID           19 // Serial 1 from ID-20 reader
#define TP_PIN_FLOW_METER_1   20 // Interrupt 3 for Swiss Flow Meter SF800
#define TP_PIN_FLOW_METER_2   21 // Interrupt 2 for Swiss Flow Meter SF800

//--- Interrupt Numbers
#define TP_INTERRUPT_FLOW_METER_1 3 // Pin D20
#define TP_INTERRUPT_FLOW_METER_2 2 // Pin D21

//--- Tapkick Constants
#define TAP_DELAY  20
#define LCD_ROWS   4
#define LCD_COLS   20
#define FLOW_CONST 6100
